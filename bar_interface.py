import os
import plotly.graph_objects as go

def make_bar(watching, completed, onHold):
    # Define the directory path where you want to save the image
    output_directory = 'static/images'

    # Ensure the output directory exists; create it if it doesn't
    os.makedirs(output_directory, exist_ok=True)

    # Define the file path within the output directory
    file_path = os.path.join(output_directory, 'proportional_bar.png')

    # Check if the file exists and delete it if it does
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted existing file: {file_path}")

    # Sample data
    variables = {'Var1': watching, 'Var2': completed, 'Var3': onHold}
    total = sum(variables.values())
    proportions = [value / total for value in variables.values()]

    # Colors for each segment
    colors = ['#ff9999', '#99ff99', '#66b3ff']

    fig = go.Figure()

    for variable, proportion, color in zip(variables.keys(), proportions, colors):
        fig.add_trace(go.Bar(
            x=[proportion],
            y=[''],
            name=variable,
            orientation='h',
            marker=dict(color=color),
            hoverinfo='x+y+name',
            showlegend=False  # Remove legend
        ))

    fig.update_layout(
        barmode='stack',
        yaxis=dict(
            showticklabels=False,  # Hide y-axis ticks
            showgrid=False,  # Hide y-axis grid
            zeroline=False  # Hide y-axis zero line
        ),
        xaxis=dict(
            showticklabels=False,  # Hide x-axis ticks
            showgrid=False,  # Hide x-axis grid
            zeroline=False  # Hide x-axis zero line
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        margin=dict(l=0, r=0, t=0, b=0)  # No margins
    )

    # Set figure size
    fig.update_layout(width=400, height=50)  # Adjust width and height to make it skinny

    # Save the figure as a PNG file with a transparent background
    fig.write_image(file_path, scale=2, width=400, height=50, engine='kaleido')

    print(f"Image file saved as '{file_path}'")