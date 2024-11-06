import streamlit as st
import requests
from github import Github
from graphviz import Digraph

# Title and Description
st.title("Mappy | Julien Okumu")
st.write("Enter a Github repository link and token to generate a detailed visualization of its components and interactions.")

# User inputs
repo_url = st.text_input("Github Repository URL")
github_token = st.text_input("Github Token", type="password")

# URL parser function
def get_repo_name(url):
    parts = url.strip("/").split("/")
    if len(parts) >= 2:
        return f"{parts[-2]}/{parts[-1]}"
    else:
        st.error("Invalid Github URL format.")
        return None

# Flowchart generation function
def generate_flowchart(repo_name, github_token):
    try:
        # Authenticate and get repo details
        g = Github(github_token)
        repo = g.get_repo(repo_name)

        # Create a directed graph
        dot = Digraph(comment="Github Repository Structure", format="png")
        dot.attr(compound='true')

        # Define custom colors for each type of component
        ui_color = "lightblue"
        backend_color = "lightcoral"
        database_color = "lightgrey"
        auth_service_color = "yellow"

        # Create primary nodes with color customization
        dot.node("repo", repo.name, shape="box", style="filled,bold", fillcolor="lightgreen", fontsize="16")
        dot.node("ui", "UI Components", shape="folder", style="filled", fillcolor=ui_color)
        dot.node("backend", "Backend Services", shape="folder", style="filled", fillcolor=backend_color)
        dot.node("database", "Data", shape="cylinder", style="filled", fillcolor=database_color)

        # Example of colored nodes for specific components
        dot.node("auth", "Authentication Service", shape="box", style="filled", fillcolor=auth_service_color)
        dot.node("api", "API Service", shape="box", style="filled", fillcolor=backend_color)
        dot.node("db", "Database", shape="cylinder", style="filled", fillcolor=database_color)

        # Example edges to show intercations
        dot.edge("repo", "ui", label="contains")
        dot.edge("repo", "backend", label="contains")
        dot.edge("backend", "auth", label="provides auth")
        dot.edge("auth", "db", label="stores data")
        dot.edge("backend", "database", label="interacts with")

        # Retrieve information like services, databases etc, from the repo files
        for content_file in repo.get_contents(""):
            file_color = ui_color if content_file.name.lower().endswith(".js") else backend_color
            dot.node(content_file.name, content_file.name, shape="note", style="filled", fillcolor=file_color)
            dot.edge("repo", content_file.name)

        return dot

    # Handle potential errors during API calls
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Generate and display the flowchart
if repo_url and github_token:
    repo_name = get_repo_name(repo_url)
    if repo_name:
        with st.spinner("Generating flowchart..."):
            dot = generate_flowchart(repo_name, github_token)
            if dot:
                st.image(dot.pipe(), use_column_width=True)
