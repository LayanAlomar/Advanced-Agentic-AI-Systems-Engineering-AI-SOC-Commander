# Resubmission Checklist

- [ ] Set `GOOGLE_API_KEY` only in the Colab runtime or local `.env`
- [ ] Run the notebook top-to-bottom
- [ ] Confirm Gemini made real function calls
- [ ] Confirm the blocked prompt-injection output appears
- [ ] Confirm the reviewer retry appears
- [ ] Confirm the HITL pause and approved resume appear
- [ ] Confirm the HITL rejected path appears
- [ ] Confirm persistence after graph recreation
- [ ] Save the notebook with execution counts and outputs
- [ ] Add `soc_events.jsonl` and `execution_summary.json` to `evidence/`
- [ ] Add screenshots to `evidence/screenshots/`
- [ ] Commit fixes incrementally using meaningful messages
- [ ] Verify README states August 2026 session dates
- [ ] Never commit `.env` or API keys
