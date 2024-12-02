from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

def query_wikidata_websites_to_csv(csv_file_path):
    # Initialize the SPARQL wrapper with the Wikidata endpoint
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    # Define the SPARQL query
    query = """
    SELECT ?entity ?entityLabel ?website WHERE {
        ?entity wdt:P31/wdt:P279* wd:Q17232649.
        ?entity wdt:P856 ?website.
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    # Prepare data for DataFrame
    data = []
    for result in results["results"]["bindings"]:
        entity = result["entity"]["value"]
        entity_label = result["entityLabel"]["value"]
        website = result["website"]["value"]
        data.append({"Entity": entity, "Entity Label": entity_label, "Website": website})

    # Create DataFrame
    df = pd.DataFrame(data)

    # Output to CSV
    df.to_csv(csv_file_path, index=False)
    print(f"Results have been saved to {csv_file_path}")

if __name__ == "__main__":
    query_wikidata_websites_to_csv("wikidata_websites.csv")
