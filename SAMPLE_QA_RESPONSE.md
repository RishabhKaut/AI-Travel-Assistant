# Sample Questions and Expected Application Behaviour

Below are the questions and response return based on data, rag, llm and mcp tool used.

---

### 1. Pure RAG — destination knowledge

**Q: "What are the must-visit attractions in Singapore?"**

- Tools called: `search_travel_knowledge_base`
- Response:
            Here are some must-visit attractions in Singapore:

            1. **Marina Bay**: This area is the modern civic and financial core of Singapore. Key sights include:
              - **Marina Bay Sands**: An integrated resort with a rooftop observation deck.
              - **Gardens by the Bay**: A large park featuring the Supertree Grove and climate-controlled conservatories (Flower Dome and Cloud Forest).
              - **Merlion Park**: Home to the iconic Merlion statue, a symbol of Singapore.
              - The waterfront promenade is great for evening walks, and you can catch the Spectra light-and-water show nightly.

            2. **Sentosa Island**: A resort island accessible by cable car or monorail, featuring attractions like:
              - **Universal Studios Singapore**
              - **S.E.A. Aquarium**
              - Various beaches and the Skyline Luge.

            3. **Singapore Zoo, River Wonders, and Night Safari**: Located in the Mandai wildlife precinct, these attractions are mostly outdoor and ideal for nature lovers.

            4. **Orchard Road**: Singapore's main shopping belt, lined with numerous malls such as ION Orchard and Paragon, perfect for shopping enthusiasts.

            5. **Kampong Glam and Little India**: Cultural districts featuring vibrant street art, cafes, and temples. Notable sites include the Sultan Mosque in Kampong Glam and the Sri Veeramakaliamman Temple in Little India.

            6. **Indoor Attractions**: For rainy days, consider visiting:
              - National Gallery Singapore
              - ArtScience Museum
              - Singapore Science Centre
              - National Museum of Singapore
              - Asian Civilisations Museum

            These attractions offer a mix of culture, entertainment, and shopping experiences, making them essential stops during your visit to Singapore.


**Q: "Suggest activities for a family with children."**
- Tools called: `search_travel_knowledge_base`
- Response:
          Here are some family-friendly activities in Singapore that are great for children:

          ### Day 1: Indoor Activities
          - **Gardens by the Bay Conservatories**: Explore the Flower Dome and Cloud Forest, which are both indoor and air-conditioned.
          - **Singapore Science Centre**: Engage with interactive exhibits that are fun and educational for children.
          - **Marina Bay Walk**: Enjoy a short outdoor stroll along the waterfront, perfect for family photos.

          ### Day 2: Outdoor Adventures
          - **Singapore Zoo**: Visit one of the world's best zoos, known for its open concept and diverse animal exhibits.
          - **River Wonders**: Explore this river-themed wildlife park, which includes a giant panda forest and various aquatic animals.

          ### Day 3: Sentosa Island
          - **S.E.A. Aquarium**: Discover marine life at one of the largest aquariums in the world.
          - **Beaches**: Spend some time relaxing at the family-friendly beaches on Sentosa.
          - **Skyline Luge**: Enjoy a fun ride down the luge track, suitable for children and adults alike.

          ### Rainy Day Backup Plan
          If the weather turns wet, consider visiting:
          - **National Gallery Singapore**
          - **ArtScience Museum**
          - **Indoor attractions at Orchard Road malls**

          These activities cater well to families and ensure that children have a memorable experience in Singapore.

**Q: "What indoor attractions can I visit?"**
- Tools called: `search_travel_knowledge_base`
- Response:
            Here are some great indoor attractions you can visit in Singapore:

            1. **National Gallery Singapore**: Explore a vast collection of Singaporean and Southeast Asian art housed in a beautifully restored historic building.

            2. **ArtScience Museum**: This museum features exhibitions that blend art, science, culture, and technology, making it a unique experience for visitors.

            3. **Gardens by the Bay Conservatories**: Visit the Flower Dome and Cloud Forest, both of which are climate-controlled and showcase a variety of plant species.

            4. **Singapore Science Centre**: Engage with interactive exhibits and learn about science and technology in a fun and educational environment.

            5. **National Museum of Singapore**: Discover the history and culture of Singapore through various exhibits and multimedia presentations.

            6. **Asian Civilisations Museum**: This museum focuses on the rich cultural heritage of Asia, showcasing artifacts and exhibitions from various Asian civilizations.

            7. **Shopping Malls along Orchard Road**: Explore the numerous malls such as ION Orchard and Paragon, which offer shopping, dining, and entertainment options all under one roof.

            These indoor attractions are perfect for escaping the heat or rain while enjoying Singapore's rich culture and entertainment.

            Sources: Singapore Attractions and Neighbourhoods (https://en.wikivoyage.org/wiki/Singapore); Sample Singapore Itineraries (https://www.visitsingapore.com/see-do-singapore/uniquely-singapore/itineraries/)

---

### 2. Pure MCP — current information

**Q: "What's the weather in Singapore right now?"**
- Tools called: `get_weather_forecast`
- Response:
  Currently, the weather in Singapore is partly cloudy with a temperature of 26.2°C. There is no precipitation at the moment.

  However, the forecast for today indicates a high of 31.7°C and a low of 24.8°C, with a 97% chance of thunderstorms later in the day.

  According to the current weather tool, please be prepared for possible rain if you're planning outdoor activities.            

**Q: "Convert INR 50,000 to SGD."**
- Tools called: `convert_currency`
- Response:

**Q: "What is the forecast for the next three days? Should I plan indoor or outdoor activities tomorrow?"**
- Tools called: `get_weather_forecast(days=3)`
- Response:
  The conversion of INR 50,000 to SGD is approximately SGD 666.50, based on the current exchange rate of 1 INR = 0.01333 SGD.

  This information comes from a live currency conversion tool.

---

### 3. Combined RAG + MCP (primary scenario)

**Q: "Plan a three-day trip to Singapore and adjust the activities based on the weather forecast."**

- Tools called: `search_travel_knowledge_base`, then `get_weather_forecast(days=3)`
- Response:
          Based on the current weather forecast, which indicates a high chance of thunderstorms later in the day, here’s a three-day trip itinerary for Singapore that includes both indoor and outdoor activities:

        ### Day 1: Indoor Activities
        - **Morning**: 
          - **Gardens by the Bay Conservatories**: Start your day exploring the Flower Dome and Cloud Forest.
        - **Afternoon**: 
          - **Singapore Science Centre**: Engage with interactive exhibits that are fun for the whole family.
        - **Evening**: 
          - **Marina Bay Walk**: If the weather permits, enjoy a short stroll along the waterfront. If it rains, consider dining at one of the indoor restaurants in Marina Bay Sands.

        ### Day 2: Outdoor Activities (Weather Permitting)
        - **Morning**: 
          - **Singapore Zoo**: Visit the zoo early in the day to avoid the heat and enjoy the open concept.
        - **Afternoon**: 
          - **River Wonders**: Explore the river-themed wildlife park. If it starts to rain, you can head to the indoor exhibits.
        - **Evening**: 
          - **Night Safari**: If the weather is clear, enjoy this unique nocturnal experience. If thunderstorms are expected, consider rescheduling for another evening.

        ### Day 3: Indoor and Outdoor Mix
        - **Morning**: 
          - **S.E.A. Aquarium**: Spend the morning indoors exploring one of the largest aquariums in the world.
        - **Afternoon**: 
          - **Sentosa Beaches**: If the weather is good, relax at the beaches. If it rains, you can visit the indoor attractions at Sentosa, such as Universal Studios Singapore (if you have tickets) or other indoor play areas.
        - **Evening**: 
          - **Skyline Luge**: If the weather is clear, enjoy this fun ride. If not, consider dining at one of the indoor restaurants on Sentosa.

        This itinerary balances indoor and outdoor activities, allowing for flexibility based on the weather conditions. Be sure to check the forecast daily and adjust your plans accordingly!

        Sources: Culture and Practical Travel Tips (https://www.visitsingapore.com/travel-guide-tips/essential-info/); Sample Singapore Itineraries (https://www.visitsingapore.com/see-do-singapore/uniquely-singapore/itineraries/); Singapore Attractions and Neighbourhoods (https://en.wikivoyage.org/wiki/Singapore)

**Q: "I have a budget of INR 60,000. Convert it to SGD and suggest a three-day itinerary."**
- Tools called: `convert_currency`, `search_travel_knowledge_base`
- Response:
          Your budget of INR 60,000 converts to approximately SGD 799.80 [Live tool result].

          Here’s a suggested three-day itinerary for your trip to Singapore:

          ### Day 1 - Marina Bay and Civic District
          - **Morning:** Visit Merlion Park and enjoy a waterfront walk at Marina Bay (outdoor).
          - **Midday:** Explore the National Gallery Singapore or the Asian Civilisations Museum (indoor).
          - **Afternoon:** Discover Gardens by the Bay, including the Supertree Grove and the Flower Dome / Cloud Forest conservatories (outdoor and indoor).
          - **Evening:** Watch the Spectra light show at Marina Bay Sands (outdoor) and have dinner at Lau Pa Sat hawker centre (semi-outdoor, covered).

          ### Day 2 - Culture: Chinatown, Little India, Kampong Glam
          - **Morning:** Visit the Buddha Tooth Relic Temple and explore Chinatown Street Market (mostly outdoor/covered market).
          - **Midday:** Enjoy lunch at Maxwell Food Centre (semi-outdoor, covered).
          - **Afternoon:** Head to Little India to see the Sri Veeramakaliamman Temple and Tekka Centre (indoor and covered).
          - **Evening:** Explore Kampong Glam, visiting the Sultan Mosque, Arab Street, and Haji Lane cafes (mixed).

          ### Day 3 - Sentosa Island
          - **Full Day:** Spend the day at Sentosa Island, where you can enjoy the beaches, visit the S.E.A. Aquarium (indoor), and experience the Skyline Luge (mixed indoor/outdoor). Alternatively, you could visit the Singapore Zoo or River Wonders if you prefer a wildlife experience.

          This itinerary offers a mix of cultural, outdoor, and indoor activities, ensuring a well-rounded experience in Singapore.

          Sources:
          - Sample Singapore Itineraries (https://www.visitsingapore.com/see-do-singapore/uniquely-singapore/itineraries/)
          - Singapore Attractions and Neighbourhoods (https://en.wikivoyage.org/wiki/Singapore)

**Q: "Suggest outdoor attractions and replace them with indoor options if rain is expected."**
- Tools called: `search_travel_knowledge_base`, `get_weather_forecast`
- Response:
          The weather forecast indicates that there will be thunderstorms expected on September 19 and 20, with a high probability of rain. On September 21, there may be slight rain showers [Live tool result]. 

          Here are some outdoor attractions along with suggested indoor alternatives in case of rain:

          ### Day 1 - Marina Bay and Civic District
          - **Outdoor Attraction:** 
            - **Merlion Park** - Iconic symbol of Singapore.
            - **Marina Bay waterfront walk** - Scenic views of the bay.
          - **Indoor Alternative (if rain):**
            - **ArtScience Museum** - Explore exhibitions on art, science, and technology.

          ### Day 2 - Culture: Chinatown, Little India, Kampong Glam
          - **Outdoor Attraction:**
            - **Buddha Tooth Relic Temple** - Beautiful temple in Chinatown.
            - **Chinatown Street Market** - Vibrant market atmosphere.
          - **Indoor Alternative (if rain):**
            - **National Gallery Singapore** - Home to a vast collection of Singaporean and Southeast Asian art.

          ### Day 3 - Sentosa Island
          - **Outdoor Attraction:**
            - **Sentosa Beaches** - Relax on the sandy shores.
            - **Skyline Luge** - Thrilling outdoor ride.
          - **Indoor Alternative (if rain):**
            - **S.E.A. Aquarium** - One of the largest aquariums in the world, showcasing marine life.

          This plan allows you to enjoy the outdoor attractions while having suitable indoor options ready in case of rain.

**Q: "Plan a family trip and include the latest weather forecast."**
- Tools called: `search_travel_knowledge_base` (family itinerary), `get_weather_forecast`
- Response:
          Here's a family-friendly three-day itinerary for your trip to Singapore, along with the latest weather forecast:

          ### Weather Forecast
          - **September 19:** Thunderstorms expected with a 97% chance of precipitation.
          - **September 20:** Thunderstorms expected with a 100% chance of precipitation.
          - **September 21:** Slight rain showers expected with a 90% chance of precipitation. [Live tool result]

          ### Family-Friendly Itinerary

          #### Day 1 - Gardens by the Bay and Marina Bay
          - **Morning:** Visit the **Gardens by the Bay** conservatories (indoor).
          - **Midday:** Explore the **Singapore Science Centre** (indoor).
          - **Afternoon:** Enjoy a short walk at **Marina Bay** (outdoor).
          - **Evening:** Watch the **Spectra light show** at Marina Bay Sands (outdoor) and have dinner at **Lau Pa Sat hawker centre** (semi-outdoor, covered).

          #### Day 2 - Wildlife Adventure
          - **Full Day:** Visit the **Singapore Zoo** and **River Wonders** (outdoor). If it rains, consider visiting the **National Gallery Singapore** or **ArtScience Museum** as indoor alternatives.

          #### Day 3 - Sentosa Island
          - **Morning:** Spend time at the **S.E.A. Aquarium** (indoor).
          - **Afternoon:** Relax on the **Sentosa beaches** (outdoor) or enjoy the **Skyline Luge** (outdoor). If rain is expected, you can opt for indoor attractions like **Universal Studios Singapore** or other indoor play areas.

          ### Rainy-Day Backup Plan
          If rain disrupts your outdoor plans, you can swap outdoor activities for:
          - **National Gallery Singapore**
          - **ArtScience Museum**
          - **Gardens by the Bay conservatories**
          - **Singapore Science Centre**
          - **Orchard Road malls** (for shopping and dining)

          This itinerary ensures a mix of fun, educational, and relaxing activities suitable for the whole family while being prepared for rainy weather. 

          Sources:
          - Sample Singapore Itineraries (https://www.visitsingapore.com/see-do-singapore/uniquely-singapore/itineraries/)
          - Culture and Practical Travel Tips (https://www.visitsingapore.com/travel-guide-tips/essential-info/)
          - Singapore Attractions and Neighbourhoods (https://en.wikivoyage.org/wiki/Singapore)

**Q: "Create a cultural itinerary and show my budget in the destination currency."**
- Tools called: `search_travel_knowledge_base` (Chinatown/Little India/Kampong
  Glam cultural itinerary), `convert_currency`
- Response:
          Here’s a cultural itinerary for your trip to Singapore, along with your budget in the destination currency:

          ### Your Budget
          Your budget of INR 60,000 converts to approximately **SGD 799.80** [Live tool result].

          ### Cultural Itinerary

          #### Day 1 - Marina Bay and Civic District
          - **Morning:** Visit the **Merlion Park** and enjoy a waterfront walk at **Marina Bay** (outdoor).
          - **Midday:** Explore the **National Gallery Singapore** or the **Asian Civilisations Museum** (indoor).
          - **Afternoon:** Discover **Gardens by the Bay**, including the Supertree Grove (outdoor) and the Flower Dome / Cloud Forest conservatories (indoor).
          - **Evening:** Watch the **Spectra light show** at Marina Bay Sands (outdoor) and have dinner at **Lau Pa Sat hawker centre** (semi-outdoor, covered).

          #### Day 2 - Cultural Exploration
          - **Morning:** Visit the **Buddha Tooth Relic Temple** and explore the **Chinatown Street Market** (mostly outdoor/covered market).
          - **Midday:** Enjoy lunch at **Maxwell Food Centre** (semi-outdoor, covered).
          - **Afternoon:** Head to **Little India** to see the **Sri Veeramakaliamman Temple** and **Tekka Centre** (indoor and covered).
          - **Evening:** Explore **Kampong Glam**, visiting the **Sultan Mosque**, Arab Street, and Haji Lane cafes (mixed).

          #### Day 3 - Sentosa Island
          - **Full Day:** Spend the day at **Sentosa Island**, where you can visit the **S.E.A. Aquarium** (indoor) and relax on the **Sentosa beaches** (outdoor). Alternatively, you can enjoy the **Skyline Luge** (outdoor). If it rains, consider visiting **Universal Studios Singapore** or other indoor attractions.

          This itinerary provides a rich cultural experience while allowing for flexibility in case of rain. Enjoy your trip! 

          Sources:
          - Sample Singapore Itineraries (https://www.visitsingapore.com/see-do-singapore/uniquely-singapore/itineraries/)
          - Singapore Attractions and Neighbourhoods (https://en.wikivoyage.org/wiki/Singapore)

---

### 4. Handling missing knowledge / tool failure gracefully

**Q: "What vaccinations do I need before visiting Singapore?"** (not covered
by the knowledge base)
- Tool called: `search_travel_knowledge_base` → returns
  `NO_RELEVANT_CONTENT: ...`
- Response:
          The knowledge base does not have specific information regarding vaccinations required before visiting Singapore. However, it is generally recommended for travelers to be up-to-date on routine vaccines and consider vaccinations for diseases such as:
s
          - Hepatitis A
          - Hepatitis B
          - Typhoid
          - Japanese Encephalitis (if you plan to visit rural areas)
          - Tetanus-Diphtheria-Pertussis (Tdap)

          It's advisable to consult with a healthcare provider or travel clinic for personalized recommendations based on your health history and travel plans.


**Q: any weather/currency question, with the upstream API down**
- The MCP tool raises a `RuntimeError`, which surfaces to the model as a
  tool error.
- Response:
          I apologize, but I am currently unable to retrieve the currency conversion rates. Please try again later.

---

### 5. Multi-turn context retention

**Q1 — "I'm traveling with two young kids and a budget of about 60,000 INR. Plan a 3-day Singapore trip."**
- Tools: `search_travel_knowledge_base` (family itinerary), `convert_currency`
  (INR→SGD)
- Response:
            Here’s a budget-friendly three-day itinerary for your trip to Singapore with two young kids, keeping your budget of approximately 60,000 INR (around SGD 800) in mind:

            ### Day 1: Gardens and Science
            - **Morning**: 
              - **Gardens by the Bay Conservatories**: Entry to the Flower Dome and Cloud Forest is about SGD 28 for adults and SGD 15 for children (ages 6-12). Total: SGD 86.
            - **Lunch**: 
              - **Food Court at Marina Bay**: Enjoy local dishes for about SGD 10 per person. Total for 4: SGD 40.
            - **Afternoon**: 
              - **Singapore Science Centre**: Entry is around SGD 12 for adults and SGD 8 for children. Total: SGD 40.
            - **Evening**: 
              - **Marina Bay Walk**: Free activity to enjoy the evening views.
            - **Dinner**: 
              - **Hawker Centre**: Budget around SGD 10 per person. Total for 4: SGD 40.

            **Day 1 Total**: SGD 286

            ### Day 2: Wildlife Adventure
            - **Morning**: 
              - **Singapore Zoo**: Entry is about SGD 39 for adults and SGD 25 for children. Total: SGD 128.
            - **Lunch**: 
              - **Zoo Cafeteria**: Budget around SGD 10 per person. Total for 4: SGD 40.
            - **Afternoon**: 
              - **River Wonders**: Entry is around SGD 39 for adults and SGD 25 for children. Total: SGD 128.
            - **Evening**: 
              - **Night Safari**: Entry is about SGD 49 for adults and SGD 33 for children. Total: SGD 164.
            - **Dinner**: 
              - **Food Court near the Zoo**: Budget around SGD 10 per person. Total for 4: SGD 40.

            **Day 2 Total**: SGD 700

            ### Day 3: Fun at Sentosa
            - **Morning**: 
              - **S.E.A. Aquarium**: Entry is around SGD 41 for adults and SGD 30 for children. Total: SGD 142.
            - **Lunch**: 
              - **Sentosa Food Court**: Budget around SGD 10 per person. Total for 4: SGD 40.
            - **Afternoon**: 
              - **Beach Time**: Enjoy the free beaches at Sentosa.
            - **Evening**: 
              - **Skyline Luge**: Approximately SGD 20 per person for a ride. Total for 4: SGD 80.
            - **Dinner**: 
              - **Hawker Centre on Sentosa**: Budget around SGD 10 per person. Total for 4: SGD 40.

            **Day 3 Total**: SGD 402

            ### Overall Budget Summary:
            - **Day 1 Total**: SGD 286
            - **Day 2 Total**: SGD 700
            - **Day 3 Total**: SGD 402

            ### Total Estimated Cost: SGD 1388

            ### Budget Considerations:
            - **Accommodation**: Look for family-friendly hotels or hostels that offer budget rates. Consider staying in areas like Little India or Chinatown for affordable options.
            - **Transportation**: Use public transport (MRT and buses) which is budget-friendly and convenient. A Singapore Tourist Pass can be a good option for unlimited rides.
            - **Food**: Eating at hawker centres and food courts will help keep your food costs down.

            This itinerary provides a mix of indoor and outdoor activities suitable for young kids while staying within a reasonable budget. Adjust activities based on your family's interests and preferences!

**Q2 — "What's the weather looking like for those days?"** (same `session_id`)
- Tool: `get_weather_forecast`
- The agent remembers this is the same 3-day family trip from Turn 1 (no
  need to re-state the budget or "with kids") and adjusts that itinerary
  using the forecast, rather than starting over.

**Q3 — "Actually, make it a 2-day trip instead."** (same `session_id`)
- The agent retrieves knowledge base content again for a shorter itinerary
  while retaining the family/kids preference and previously converted
  budget from earlier turns.
