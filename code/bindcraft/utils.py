import os
import pandas as pd
import shutil

def rank_and_save_designs(design_paths, mpnn_csv, final_csv, final_labels, design_labels, target_settings):
    """
    Rank and save the accepted binder designs based on their scores.

    Args:
        design_paths (dict): Dictionary containing paths for design directories.
        mpnn_csv (str): Path to the MPNN design statistics CSV file.
        final_csv (str): Path to the final ranked designs CSV file.
        final_labels (list): List of column labels for the final CSV.
        design_labels (list): List of column labels for design statistics.
        target_settings (dict): Dictionary containing target settings.
    """
    accepted_binders = [f for f in os.listdir(design_paths["Accepted"]) if f.endswith('.pdb')]

    # Clear the Ranked folder
    for f in os.listdir(design_paths["Accepted/Ranked"]):
        os.remove(os.path.join(design_paths["Accepted/Ranked"], f))

    # Load and sort the dataframe of designed binders
    design_df = pd.read_csv(mpnn_csv)
    design_df = design_df.sort_values('Average_i_pTM', ascending=False)

    # Create final dataframe to store ranked designs
    final_df = pd.DataFrame(columns=final_labels)

    # Rank and copy designs to the Ranked folder
    rank = 1
    for _, row in design_df.iterrows():
        for binder in accepted_binders:
            target_settings["binder_name"], model = binder.rsplit('_model', 1)
            if target_settings["binder_name"] == row['Design']:
                # Add rank and copy to ranked folder
                row_data = {'Rank': rank, **{label: row[label] for label in design_labels}}
                final_df = pd.concat([final_df, pd.DataFrame([row_data])], ignore_index=True)
                old_path = os.path.join(design_paths["Accepted"], binder)
                new_path = os.path.join(design_paths["Accepted/Ranked"], f"{rank}_{target_settings['binder_name']}_model{model.rsplit('.', 1)[0]}.pdb")
                shutil.copyfile(old_path, new_path)

                rank += 1
                break

    # Save the final ranked designs to a CSV file
    final_df.to_csv(final_csv, index=False)

    print("Designs ranked and final_designs_stats.csv generated")


def view_top_k_designs(path=".",k=20):
    df = pd.read_csv(os.path.join(path, 'final_design_stats.csv'))
    print(df.head(k))
    print("\n\n")

#@title Display animation
import glob
# from IPython.display import HTML#@title Top Design Display
import py3Dmol

def visualize_top_design(design_path):
    """
    Visualize the top-ranked design in PyMOL using py3Dmol.

    Args:
        design_path (str): Path to the design directory.
    """
    top_design_dir = os.path.join(design_path, 'Accepted', 'Ranked')
    top_design_pdb = glob.glob(os.path.join(top_design_dir, '1_*.pdb'))[0]

    # Visualize in PyMOL
    view = py3Dmol.view()
    view.addModel(open(top_design_pdb, 'r').read(), 'pdb')
    view.setBackgroundColor('white')
    view.setStyle({'chain': 'A'}, {'cartoon': {'color': '#3c5b6f'}})
    view.setStyle({'chain': 'B'}, {'cartoon': {'color': '#B76E79'}})
    view.zoomTo()
    view.show()


# def display_top_design_animation(design_path):
#     """
#     Display the animation of the top-ranked design.

#     Args:
#         design_path (str): Path to the design directory.
#     """
#     top_design_dir = os.path.join(design_path, 'Accepted', 'Ranked')
#     top_design_pdb = glob.glob(os.path.join(top_design_dir, '1_*.pdb'))[0]

#     top_design_name = os.path.basename(top_design_pdb).split('1_', 1)[1].split('_mpnn')[0]
#     top_design_animation = os.path.join(design_path, 'Accepted', 'Animation', f"{top_design_name}.html")

#     # Show animation
#     return HTML(top_design_animation)