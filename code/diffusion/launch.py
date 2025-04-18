from argparser import *
import os
from utils import *


import sys

from colabdesign.mpnn import mk_mpnn_model
from colabdesign.af import mk_af_model
from colabdesign.shared.protein import pdb_to_string
from colabdesign.shared.parse_args import parse_args

import pandas as pd
import numpy as np
from string import ascii_uppercase, ascii_lowercase
alphabet_list = list(ascii_uppercase+ascii_lowercase)

args=parse_args()



if not os.path.isdir("outputs"):
  os.makedirs("outputs")


path = name
while os.path.exists(f"outputs/{path}_0.pdb"):
  path = name + "_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))

flags = {"contigs":args.contigs,
         "pdb":args.pdb,
         "order":args.order,
         "iterations":int(args.iterations),
         "symmetry":args.symmetry,
         "hotspot":args.hotspot,
         "path":args.path,
         "chains":args.chains,
         "add_potential":args.add_potential,
         "num_designs":args.num_designs,
         "use_beta_model":args.use_beta_model,
         "visual":args.visual,
         "partial_T":args.partial_T}

for k,v in flags.items():
  if isinstance(v,str):
    flags[k] = v.replace("'","").replace('"','')


contigs, copies = run_diffusion(**flags)

if not os.path.isfile("params/done.txt"):
  print("downloading AlphaFold params...")
  while not os.path.isfile("params/done.txt"):
    time.sleep(5)


if num_designs > 1:
  output = widgets.Output()
  def on_change(change):
    if change['name'] == 'value':
      with output:
        output.clear_output(wait=True)
        plot_pdb(change['new'])
  dropdown = widgets.Dropdown(
      options=[(f'{k}',k) for k in range(num_designs)],
      value=0, description='design:',
  )
  dropdown.observe(on_change)
  display(widgets.VBox([dropdown, output]))
  with output:
    plot_pdb(dropdown.value)
else:
  plot_pdb()


# !python colabdesign/rf/designability_test.py {opts}
#####################################################################


num_seqs = args.num_seqs
loc="outputs/{path}"
pdb="outputs/{path}_0.pdb"

contigs_str = ":".join(contigs)

rm_aa = args.rm_aa

if rm_aa == "":
    rm_aa = None

# filter contig input
contigs = []
for contig_str in contigs_str.replace(" ", ":").replace(",", ":").split(":"):
    if len(contig_str) > 0:
        contig = []
        for x in contig_str.split("/"):
            if x != "0":
                contig.append(x)
        contigs.append("/".join(contig))

chains = alphabet_list[:len(contigs)]
info = [get_info(x) for x in contigs]
fixed_pos = []
fixed_chains = []
free_chains = []
both_chains = []
for pos,(fixed_chain,free_chain) in info:
    fixed_pos += pos
    fixed_chains += [fixed_chain and not free_chain]
    free_chains += [free_chain and not fixed_chain]
    both_chains += [fixed_chain and free_chain]

flags = {"initial_guess":args.initial_guess,
        "best_metric":"rmsd",
        "use_multimer":args.use_multimer,
        "model_names":["model_1_multimer_v3" if args.use_multimer else "model_1_ptm"]}

if sum(both_chains) == 0 and sum(fixed_chains) > 0 and sum(free_chains) > 0:
    protocol = "binder"
    print("protocol=binder")
    target_chains = []
    binder_chains = []
    for n,x in enumerate(fixed_chains):
        if x: target_chains.append(chains[n])
        else: binder_chains.append(chains[n])
    af_model = mk_af_model(protocol="binder",**flags)
    prep_flags = {"target_chain":",".join(target_chains),
                  "binder_chain":",".join(binder_chains),
                  "rm_aa":rm_aa}
    opt_extra = {}

elif sum(fixed_pos) > 0:
    protocol = "partial"
    print("protocol=partial")
    af_model = mk_af_model(protocol="fixbb",
                            use_templates=True,
                            **flags)
    rm_template = np.array(fixed_pos) == 0
    prep_flags = {"chain":",".join(chains),
                    "rm_template":rm_template,
                    "rm_template_seq":rm_template,
                    "copies":copies,
                    "homooligomer":copies>1,
                    "rm_aa":rm_aa}
else:
    protocol = "fixbb"
    print("protocol=fixbb")
    af_model = mk_af_model(protocol="fixbb",**flags)
    prep_flags = {"chain":",".join(chains),
                    "copies":copies,
                    "homooligomer":copies>1,
                    "rm_aa":rm_aa}

batch_size = 8
if num_seqs < batch_size:
    batch_size = num_seqs

print("running proteinMPNN...")
sampling_temp = args.mpnn_sampling_temp
mpnn_model = mk_mpnn_model(weights="soluble" if args.use_solubleMPNN else "original")
outs = []
pdbs = []
for m in range(num_designs):
    if num_designs == 0:
        pdb_filename = pdb
    else:
        pdb_filename = pdb.replace("_0.pdb",f"_{m}.pdb")
    pdbs.append(pdb_filename)
    af_model.prep_inputs(pdb_filename, **prep_flags)
    if protocol == "partial":
        p = np.where(fixed_pos)[0]
        af_model.opt["fix_pos"] = p[p < af_model._len]

    mpnn_model.get_af_inputs(af_model)
    outs.append(mpnn_model.sample(num=num_seqs//batch_size, batch=batch_size, temperature=sampling_temp))

if protocol == "binder":
    af_terms = ["plddt","i_ptm","i_pae","rmsd"]
elif copies > 1:
    af_terms = ["plddt","ptm","i_ptm","pae","i_pae","rmsd"]
else:
    af_terms = ["plddt","ptm","pae","rmsd"]

labels = ["design","n","score"] + af_terms + ["seq"]
data = []
best = {"rmsd":np.inf,"design":0,"n":0}
print("running AlphaFold...")
os.system(f"mkdir -p {loc}/all_pdb")
with open(f"{loc}/design.fasta","w") as fasta:
    for m,(out,pdb_filename) in enumerate(zip(outs,pdbs)):
        out["design"] = []
        out["n"] = []
        af_model.prep_inputs(pdb_filename, **prep_flags)
        for k in af_terms: out[k] = []
        for n in range(num_seqs):
            out["design"].append(m)
            out["n"].append(n)
            sub_seq = out["seq"][n].replace("/","")[-af_model._len:]
            af_model.predict(seq=sub_seq, num_recycles=args.num_recycles, verbose=False)
            for t in af_terms: out[t].append(af_model.aux["log"][t])
            if "i_pae" in out:
                out["i_pae"][-1] = out["i_pae"][-1] * 31
            if "pae" in out:
                out["pae"][-1] = out["pae"][-1] * 31
            rmsd = out["rmsd"][-1]
            if rmsd < best["rmsd"]:
                best = {"design":m,"n":n,"rmsd":rmsd}
            af_model.save_current_pdb(f"{loc}/all_pdb/design{m}_n{n}.pdb")
            af_model._save_results(save_best=True, verbose=False)
            af_model._k += 1
            score_line = [f'design:{m} n:{n}',f'mpnn:{out["score"][n]:.3f}']
            for t in af_terms:
                score_line.append(f'{t}:{out[t][n]:.3f}')
            print(" ".join(score_line)+" "+out["seq"][n])
            line = f'>{"|".join(score_line)}\n{out["seq"][n]}'
            fasta.write(line+"\n")
        data += [[out[k][n] for k in labels] for n in range(num_seqs)]
        af_model.save_pdb(f"{loc}/best_design{m}.pdb")

  # save best
with open(f"{loc}/best.pdb", "w") as handle:
    remark_text = f"design {best['design']} N {best['n']} RMSD {best['rmsd']:.3f}"
    handle.write(f"REMARK 001 {remark_text}\n")
    handle.write(open(f"{loc}/best_design{best['design']}.pdb", "r").read())

labels[2] = "mpnn"
df = pd.DataFrame(data, columns=labels)
df.to_csv(f'{loc}/mpnn_results.csv')
