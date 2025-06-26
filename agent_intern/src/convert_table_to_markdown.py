from bs4 import BeautifulSoup

with open('../exhaustive-list-of-agent-frameworks.md') as f:
    html_content = f.read()

# Sample HTML content (replace this with your actual HTML content)
# html_content = """
# <!-- Your HTML content goes here -->
# """

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table
table = soup.find('table')

# Initialize a list to store the extracted data
data = []

# Iterate over each row in the table (excluding the header)
for row in table.tbody.find_all('tr')[1:]:
    # Extract the columns
    columns = row.find_all(['td', 'th'])

    # Extract the name, description, website, pricing model, and logo
    name = columns[0].text.strip()
    description = columns[1].text.strip()
    website = columns[2].find('a')['href'] if columns[2].find('a') else ''
    pricing_model = columns[3].text.strip()
    logo = columns[4].find('img')['src'] if columns[4].find('img') else ''

    # Append the extracted data to the list
    data.append({
        'name': name,
        'description': description,
        'website': website,
        'pricing_model': pricing_model,
        'logo': logo
    })

# Print the extracted data in Markdown format
print("## Extracted Data\n")
for item in sorted(data, key=lambda x: x['name']):
    print(f"### {item['name']}\n")
    print(f"- **Description**: {item['description']}")
    if item['website']:
        print(f"- **Website**: [{item['name']}](<{item['website']}>)")
    if item['logo']:
        print(f"- **Logo**: ![Logo]({item['logo']})")
    print(f"- **Pricing Model**: {item['pricing_model']}\n")