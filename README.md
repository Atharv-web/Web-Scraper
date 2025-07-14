# Reddit User Persona Generator

This project scrapes a Reddit user's comments and uses a LLM to generate a user persona based on their activity.

## Features

- Scrapes a user's most recent comments from Reddit.
- Generates a detailed user persona, including interests, tone, and profession guess.
- Cites the specific comments used to determine each trait.

## How to Use

1. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API key:**
   Add the following line to the `.env` file:

     ```
     GEMINI_API_KEY="YOUR_API_KEY"
     ```

3. **Run the scraper:**

   To scrape a specific user's comments, run the `demo_scraper.py` script and provide the user's Reddit profile URL when prompted.

     ```bash
     python demo_scraper.py
     ```

4. **Generate the persona:**

   - Once the scraper has finished, run the `persona_maker.py` script to generate the persona.

     ```bash
     python persona_maker.py
     ```

   - The persona will be saved in a text file named `persona_<username>.txt`.

