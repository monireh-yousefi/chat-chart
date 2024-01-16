# Chat Chart

Chat-Chart is an innovative project at the intersection of artificial intelligence and environmental
data visualization, aiming to improve the way users interact with and comprehend complex datasets.

Leveraging Language Model (LLM) capabilities, Chat-Chart enables users to effortlessly convert natural
language queries into structured SQL queries. The query is then executed on a database which contains
a subset of (global air pollution
dataset)[https://www.kaggle.com/datasets/hasibalmuzdadid/global-air-pollution-dataset?resource=download].
After that, we examine the result columns to select one of the line, bar or scatter charts to visualize
the table.

By combining AI-driven language processing with intuitive data representation, we can make
interacting with complex datasets such as environmental ones, much easier and accessible.
            
## Technologies Used:

- **Server:** Python, FastAPI, Docker, SQL, SQLite, SQLAlchemy
- **UI:** HTML, CSS, Bootstrap, MDB, Chart.js, Highlight.js
- **AI:** OpenAI API, GPT 3.5 Model

## Potential Research Areas:

- Using large language models to query and create insights from multiple data sources. This project only uses a single
  table in the database.
- Using AI to improve chart selection and parameter setting based on the data. In this project we are just using a
  couple of extracted properties to select the chart. But this can be improved using AI.
