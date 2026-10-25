# celebrait — Agent Rules

You are working on **celebrait**, a GenAI-powered event planner for weddings, birthdays, and community events.

## Project goal

Build a simple, reliable Streamlit web app that generates:

- Personalized event concepts
- Budget plans
- Planning timelines
- Vendor checklists
- Day-of-event schedules
- Risk checklists
- Money-saving tips

## Tech stack

- Python
- Streamlit
- Google Gemini API using the `google-genai` package
- Git and GitHub
- Streamlit Community Cloud for deployment

Do not introduce additional frameworks, databases, payment systems, authentication systems, or complex cloud services unless explicitly requested.

## Coding standards

- Write beginner-friendly, readable Python.
- Use clear function and variable names.
- Add short comments only where they explain non-obvious logic.
- Keep `app.py` organized with sections for UI, input validation, prompt creation, and Gemini API call.
- Use Streamlit widgets and layout correctly.
- Handle user errors gracefully with `st.error()` or `st.warning()`.
- Do not use print statements for user-facing output; use Streamlit UI elements.

## Gemini API rules

- Read the API key from the `GEMINI_API_KEY` environment variable.
- Never hardcode, display, log, or commit an API key.
- Show a clear error if the API key is missing.
- Use a structured prompt that requests Markdown output.
- Clearly state that vendor names, prices, and availability are estimates and must be verified locally.
- Do not claim AI-generated information is guaranteed or official.

## Git and security rules

- Never commit `.env`, `.streamlit/secrets.toml`, API keys, passwords, virtual environments, videos, datasets, or generated PDFs.
- Respect the existing `.gitignore`.
- Before committing, check `git status` and ensure only intended project files are staged.
- Keep the repository under 10 MB.
- Write concise conventional commit messages, for example:
  - `feat: add event plan generator`
  - `fix: handle missing Gemini API key`
  - `docs: update README setup steps`

## Development workflow

1. Understand the requested change.
2. Make the smallest useful change.
3. Explain what you changed in simple language.
4. Do not change unrelated files or refactor the entire project unless asked.
5. After code changes, provide the exact command to test locally:

   ```bash
   streamlit run app.py
   ```

6. If an error occurs, identify the exact cause before changing code.
7. Do not invent package names, API methods, or commands.

## UI rules

- Keep the interface clean and beginner-friendly.
- Use a sidebar for event inputs.
- Use clear labels, placeholders, and helpful validation messages.
- Use Markdown tables for budget and vendor checklists.
- Provide a download button for the generated event plan.
- Make the app usable on both desktop and mobile.

## Submission rules

The final repository must:

- Be public on GitHub.
- Be under 10 MB.
- Contain a complete `README.md`.
- Contain `requirements.txt`.
- Not contain API keys or private credentials.
- Include setup and deployment instructions.
