import argparse
import os
import json
from datetime import datetime

def getArgs():
    parser = argparse.ArgumentParser(description="Binder design settings for BindCraft")

    # Binder design settings
    parser.add_argument("--design_path", type=str, default="./content/drive/MyDrive/BindCraft/PDL1/",
                        help="Path where to save your designs.")
    parser.add_argument("--binder_name", type=str, default="PDL1",
                        help="Name to prefix to your binders (generally target name).")
    parser.add_argument("--starting_pdb", type=str, default="./content/bindcraft/example/PDL1.pdb",
                        help="Path to the .pdb structure of your target.")
    parser.add_argument("--chains", type=str, default="A",
                        help="Chains of your PDB to target (comma-separated).")
    parser.add_argument("--target_hotspot_residues", type=str, default="",
                        help="Positions to target in your protein of interest.")
    parser.add_argument("--lengths", type=str, default="70,150",
                        help="Minimum and maximum size of binders to design (comma-separated).")
    parser.add_argument("--number_of_final_designs", type=int, default=100,
                        help="Number of binder designs passing filters required.")
    parser.add_argument("--load_previous_target_settings", type=str, default="",
                        help="Path to previous target settings to continue design campaign.")

    # Advanced settings
    parser.add_argument("--design_protocol", type=str, choices=["Default", "Beta-sheet", "Peptide"],
                        default="Default", help="Binder design protocol to run.")
    parser.add_argument("--prediction_protocol", type=str, choices=["Default", "HardTarget"],
                        default="Default", help="Prediction protocol to use.")
    parser.add_argument("--interface_protocol", type=str, choices=["AlphaFold2", "MPNN"],
                        default="AlphaFold2", help="Interface design method to use.")
    parser.add_argument("--template_protocol", type=str, choices=["Default", "Masked"],
                        default="Default", help="Target template protocol to use.")

    # Filters
    parser.add_argument("--filter_option", type=str,
                        choices=["Default", "Peptide", "Relaxed", "Peptide_Relaxed", "None"],
                        default="Default", help="Filters for designs to use.")

    args = parser.parse_args()

    # Process lengths
    if args.load_previous_target_settings:
        target_settings_path = args.load_previous_target_settings
    else:
        lengths = [int(x.strip()) for x in args.lengths.split(',') if len(args.lengths.split(',')) == 2]

        if len(lengths) != 2:
            raise ValueError("Incorrect specification of binder lengths.")

        settings = {
            "design_path": args.design_path,
            "binder_name": args.binder_name,
            "starting_pdb": args.starting_pdb,
            "chains": args.chains,
            "target_hotspot_residues": args.target_hotspot_residues,
            "lengths": lengths,
            "number_of_final_designs": args.number_of_final_designs
        }

        target_settings_path = os.path.join(args.design_path, args.binder_name + ".json")
        os.makedirs(args.design_path, exist_ok=True)

        with open(target_settings_path, 'w') as f:
            json.dump(settings, f, indent=4)

    currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Binder design settings updated at: {currenttime}")
    print(f"New .json file with target settings has been generated in: {target_settings_path}")

    # Advanced settings processing
    if args.design_protocol == "Default":
        design_protocol_tag = "default_4stage_multimer"
    elif args.design_protocol == "Beta-sheet":
        design_protocol_tag = "betasheet_4stage_multimer"
    elif args.design_protocol == "Peptide":
        design_protocol_tag = "peptide_3stage_multimer"
    else:
        raise ValueError(f"Unsupported design protocol")

    if args.interface_protocol == "AlphaFold2":
        interface_protocol_tag = ""
    elif args.interface_protocol == "MPNN":
        interface_protocol_tag = "_mpnn"
    else:
        raise ValueError(f"Unsupported interface protocol")

    if args.template_protocol == "Default":
        template_protocol_tag = ""
    elif args.template_protocol == "Masked":
        template_protocol_tag = "_flexible"
    else:
        raise ValueError(f"Unsupported template protocol")

    if args.design_protocol in ["Peptide"]:
        prediction_protocol_tag = ""
    else:
        if args.prediction_protocol == "Default":
            prediction_protocol_tag = ""
        elif args.prediction_protocol == "HardTarget":
            prediction_protocol_tag = "_hardtarget"
        else:
            raise ValueError(f"Unsupported prediction protocol")

    advanced_settings_path = "./content/bindcraft/settings_advanced/" + design_protocol_tag + interface_protocol_tag + template_protocol_tag + ".json"

    currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Advanced design settings updated at: {currenttime}")

    # Filters processing
    if args.filter_option == "Default":
        filter_settings_path = "./content/bindcraft/settings_filters/default_filters.json"
    elif args.filter_option == "Peptide":
        filter_settings_path = "./content/bindcraft/settings_filters/peptide_filters.json"
    elif args.filter_option == "Relaxed":
        filter_settings_path = "./content/bindcraft/settings_filters/relaxed_filters.json"
    elif args.filter_option == "Peptide_Relaxed":
        filter_settings_path = "./content/bindcraft/settings_filters/peptide_relaxed_filters.json"
    elif args.filter_option == "None":
        filter_settings_path = "./content/bindcraft/settings_filters/no_filters.json"
    else:
        raise ValueError(f"Unsupported filter type")

    currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Filter settings updated at: {currenttime}")

    # Save the advanced settings to a JSON file
    advanced_settings = {
        "design_protocol": design_protocol_tag,
        "interface_protocol": interface_protocol_tag,
        "template_protocol": template_protocol_tag,
        "prediction_protocol": prediction_protocol_tag,
        "filters": filter_settings_path,
        "settings": target_settings_path,
        "advanced": advanced_settings_path,

    }
    return advanced_settings

if __name__ == "__main__":
    getArgs()
