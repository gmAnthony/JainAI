# What the heck is JainAI?

JainAI is an AI-powered slack bot that I created for my fantasy basketball league. It takes in our league's constitution and uses it as context when members of the league ask questions relevant to the league's rules. The constitution is a PDF that is sectioned out and embeddings are generated for those sections. The embeddings are then uploaded to a Pinecone DB which is then referenced when Jain is queried in Slack. Jain is powered by ChatGPT.
