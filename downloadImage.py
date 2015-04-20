from gilt.rest import GiltApiClient
import urllib

# Create client using api_key
client = GiltApiClient(api_key = '4bc9ea982749056525a630ff9eb6deda9f737c2a94492963f29e32f077ed766f')

# Get Active Sales info, go to men store, need to check what sales there are
for sale in client.sales.active('men'):
  print 'Number of sales: ', len(client.sales.active('men'))
  # Select how many products do you want
  product_urls = sale.products[0:1]
  if not product_urls: continue
  print 'First %d products (of %d) of sale "%s"' % (len(product_urls), len(sale.products), sale.name)
  # For each product  
  for url in product_urls:
    product = client.products.get(url=url) 
    # Get image url
    for image in product.image_urls.image_list("300x400"):
      print image.url
      urllib.urlretrieve(image.url, "cloth.jpg")
      break #only do one image
  break # only do one sale

