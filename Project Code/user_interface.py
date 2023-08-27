# interface.py
import gradio as gr  # Import the Gradio library
from ndvi_calculator import calculate_ndvi  # Import the calculate_ndvi function from the index_calculator module
import earthpy.plot as ep
import cv2

# Define the process_file function that takes two file objects as inputs
def process_file(red_band_file, nir_band_file, visualize_button): 
    red_band_path = red_band_file.name  # Get the file path from the first file object
    nir_band_path = nir_band_file.name  # Get the file path from the second file object
    
    # Calculate NDVI using the calculate_ndvi function
    avg_ndvi, min_ndvi, max_ndvi, ndvi_category, hist_path, average_ndvi_path = calculate_ndvi(red_band_path, nir_band_path)
    # hist_image = cv2.imread(hist_path, 1)
    # average_ndvi_image = cv2.imread(average_ndvi_path, 1)
    return avg_ndvi, min_ndvi, max_ndvi, ndvi_category # Return the calculated NDVI result

    # For Plots : 
    """ if visualize_button:
        # Create the NDVI plot
        titles = ["Vegetation Health Assessment using NDVI"]
        plot = ep.plot_bands(ndvi, cmap="RdYlGn", cols=1, title=titles, vmin=-1, vmax=1, figsize=(5, 5))
        # return f"Average NDVI: {avg_ndvi}\nMinimum NDVI: {min_ndvi}\nMaximum NDVI: {max_ndvi}", ndvi_category, plot
        return avg_ndvi, min_ndvi, max_ndvi, ndvi_category, plot
    else:
        return avg_ndvi, min_ndvi, max_ndvi, ndvi_category """

# Check if the module is run as the main program
if __name__ == "__main__":
    # Create a Gradio interface
    demo = gr.Interface(
        fn=process_file,  # Use the process_file function for processing inputs
        inputs=[
            gr.inputs.File(label="Red Band TIFF"),
            gr.inputs.File(label="NIR Band TIFF"),
            # gr.inputs.Checkbox(label="Visualize")  # Checkbox input for visualization
            ],  # Define two file input fields
        outputs=[
            gr.Textbox(label="Average NDVI"),  # Label for the Average NDVI output
            gr.Textbox(label="Minimum NDVI"),  # Label for the Minimum NDVI output
            gr.Textbox(label="Maximum NDVI"),  # Label for the Maximum NDVI output
            gr.Textbox(lines = 3, label="Category"),   # Label for the NDVI Category output
            # gr.Image(),
            # gr.Image()
            # gr.Image(label="NDVI Plot")        # Image output for NDVI plot
        ],  # Define the output field type as text
        flagging_options=["Save"], # Change the text of the flag button
        title="Vegetation Mapping Using NDVI"
    )
    
    # Launch the Gradio interface
    demo.launch(share = True)




