# Gruber Klaviyo Demo

The objective of this script is to send targeted emails to customers based off of the current whether in their location. The idea behind this is that there is a demand for industries such as outdoor stores, fashion, hardware, etc. based on the weather or season. What better time to sell to a customer than right before a snowstorm or a big rain storm when they are in need of a product such as an umbrella or a snow shovel. We want to make sure that our customers are the first ones to reach out to ensure their customers buy these products from them.

What I've done is create a segment of all profiles that have a location associated. Using that location, the script call and open weather API to get the current weather for each location and that creates a tracking metric called "Weather Udate" and update a property in that metric called "current_weather". I've put together a flow that is triggered via the "Weather Update" metric and depending on the value of "current_weather" that is passed, an email targeting the customer with a product based on their weather is sent to them. If it's raining then the customer will receive an emai to buy an umbrella, if it's snowing they will receive and email for snow shovels, and if it's sunny out, then they will receive and email for sunglasses.

After writing this script i've thought through some ways this can be used in the real world. Ideally, we would want our customer to be able to send these emails a few days ahead of time since it does do any good to buy an umbrella once it's already raining. The script would essentially be the same except instead of hitting the `/current` endpoint when retrieving the weather, we would hit the `/forecast?access_key={{YOUR_ACCESS_KEY}}& query={{city}}&forecast_days = 3` to be able to send an email 3 days before its going to rain to give the customer time to buy an umbrella.

As a customer, I won't want to be getting these emails all the time or else I would unsubscribe pretty quickly. I've set up my flow to have a conditional split that won't send an email to someone who has already received it in the last 30 days to prevent a high unsubscription rate.

The script would be on a schedule to run once a day via a cron to account for any new profiles created.  