import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Run RFdiffusion, ProteinMPNN, and AlphaFold for protein design.")

    # RFdiffusion settings
    parser.add_argument("--name", type=str, default="test", help="Name of the run.")
    parser.add_argument("--contigs", type=str, default="100", help="Contigs for the design.")
    parser.add_argument("--pdb", type=str, default="", help="Path to the PDB file.")
    parser.add_argument("--iterations", type=int, choices=[25, 50, 100, 150, 200], default=50, help="Number of iterations.")
    parser.add_argument("--hotspot", type=str, default="", help="Hotspot residues.")
    parser.add_argument("--num_designs", type=int, choices=[1, 2, 4, 8, 16, 32], default=1, help="Number of designs to generate.")
    parser.add_argument("--visual", type=str, choices=["none", "image", "interactive"], default="image", help="Visualization mode.")

    # Symmetry settings
    parser.add_argument("--symmetry", type=str, choices=["none", "auto", "cyclic", "dihedral"], default="none", help="Symmetry mode.")
    parser.add_argument("--order", type=int, choices=list(range(1, 13)), default=1, help="Symmetry order.")
    parser.add_argument("--chains", type=str, default="", help="Chains to filter PDB input.")
    parser.add_argument("--add_potential", action="store_true", help="Add potential to discourage clashes between chains.")

    # Advanced settings
    parser.add_argument("--partial_T", type=str, choices=["auto", "10", "20", "40", "60", "80"], default="auto", help="Number of noising steps for partial diffusion.")
    parser.add_argument("--use_beta_model", action="store_true", help="Use beta model for better SSE balance.")

    # ProteinMPNN settings
    parser.add_argument("--num_seqs", type=int, choices=[1, 2, 4, 8, 16, 32, 64], default=8, help="Number of sequences to generate.")
    parser.add_argument("--mpnn_sampling_temp", type=float, default=0.1, help="Sampling temperature for ProteinMPNN.")
    parser.add_argument("--rm_aa", type=str, default="C", help="Amino acids to exclude.")
    parser.add_argument("--use_solubleMPNN", action="store_true", help="Use weights trained only on soluble proteins.")

    # AlphaFold settings
    parser.add_argument("--initial_guess", action="store_true", help="Enable soft initialization with desired coordinates.")
    parser.add_argument("--num_recycles", type=int, choices=[0, 1, 2, 3, 6, 12], default=1, help="Number of recycles for AlphaFold.")
    parser.add_argument("--use_multimer", action="store_true", help="Use AlphaFold Multimer v3 parameters.")

    return parser.parse_args()#@title run **RFdiffusion** to generate a backbone






