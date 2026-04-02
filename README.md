# PagoTronic B2B

## Product Overview
PagoTronic is a unified B2B infrastructure that empowers fintechs, banks, and marketplaces to move money seamlessly. Our developer-first API unifies collections, payouts, and transfers with integrated smart routing, anti-fraud, and compliance. Orchestrate traditional and digital rails with automated reconciliation and full traceability. From MVP to global scale, PagoTronic allows you to deploy sophisticated financial services without building the infrastructure from scratch.

## Architecture Diagram
```text
+-----------------+        +--------------------------+        +--------------------------+
|                 |        |                          |        |                          |
|  Client / API   | -----> |  Cloud Run Service       | -----> |  Cloud SQL Database      |
|  (Web/Mobile)   |        |  (pagotronic-b2b-studio) |        |  (Instance: quien-prod)  |
|                 |        |                          |        |                          |
+-----------------+        +--------------------------+        +--------------------------+
                                       |  ^
                                       |  |
                                       v  |
                           +--------------------------+
                           |                          |
                           |  Stripe Billing API &    |
                           |  Webhooks Engine         |
                           |                          |
                           +--------------------------+
```

## Environment Variables Reference
To successfully run the PagoTronic B2B application, ensure the following environment variables are set in your deployment:

| Variable | Description |
|---|---|
| `WEBSITE_TAGLINE_EN` | Unified B2B payment infrastructure for fintechs, banks, and marketplaces. |
| `PRODUCT_DESCRIPTION` | PagoTronic product description text. |
| `DB_USER` | `svc_pagotronic_b2b` |
| `DB_PASSWORD_SECRET` | Secret Manager reference: `pagotronic_b2b-db-password` |
| `DB_NAME` | `pagotronic_b2b` |
| `DB_CONNECTION_NAME` | `test-agents-ai-app:us-central1:quien-prod` |
| `STRIPE_WEBHOOK_SECRET`| Stripe webhook secret (must be manually generated). |

## Deployment Instructions
*Note: The initial automated Cloud Build encountered a 403 Permission Denied error. You will need to verify Cloud Build permissions for the service account in the `sitiouno-mvpfactory` organization before retrying.*

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sitiouno-mvpfactory/pagotronic-b2b-studio.git
   cd pagotronic-b2b-studio
   ```
2. **Resolve Permissions:** Ensure your Google Cloud service account has the `Cloud Build Editor` and `Cloud Run Admin` IAM roles.
3. **Build the container image:**
   ```bash
   gcloud builds submit --tag gcr.io/[PROJECT_ID]/pagotronic-b2b-studio
   ```
4. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy pagotronic-b2b-studio \
     --image gcr.io/[PROJECT_ID]/pagotronic-b2b-studio \
     --platform managed \
     --allow-unauthenticated \
     --add-cloudsql-instances test-agents-ai-app:us-central1:quien-prod
   ```

## DNS Configuration Steps
To map the domain path `mvpfactory.studio/p/pagotronic-b2b` to your Cloud Run service:
1. Navigate to **Cloud Run** in the Google Cloud Console.
2. Select the `pagotronic-b2b-studio` service.
3. Click **Manage Custom Domains**.
4. Add a mapping for `mvpfactory.studio` and update your DNS provider with the provided A/AAAA or CNAME records.
5. *Path Routing:* Since the app uses a specific path (`/p/pagotronic-b2b`), configure an HTTP(S) Load Balancer in Google Cloud to route traffic for this URL map directly to the Cloud Run backend service.

## Stripe Webhook Setup
Stripe automatic configuration was skipped due to missing API keys. Please perform the following steps to finalize billing:
1. Log in to the [Stripe Dashboard](https://dashboard.stripe.com/).
2. Navigate to **Developers > Webhooks**.
3. Add a new endpoint URL: `https://mvpfactory.studio/p/pagotronic-b2b/api/webhooks/stripe`.
4. Select the events you wish to listen to (e.g., `payment_intent.succeeded`, `invoice.paid`).
5. Reveal the Webhook Secret (`whsec_...`) and update `STRIPE_WEBHOOK_SECRET` in your environment or within the generated `stripe_config.py` file.
6. Create your Products and Prices in Stripe, and update the placeholder `STRIPE_PRODUCT_ID` and `STRIPE_PRICE_ID` inside `stripe_config.py`.

## Monitoring and Troubleshooting
- **Application Logs:** View real-time logs in Google Cloud Logging under the Cloud Run service `pagotronic-b2b-studio`.
- **Database Metrics:** Monitor SQL queries, connections, and storage in the Cloud SQL dashboard for the instance `quien-prod`.
- **Stripe Events:** Use the Stripe Dashboard's "Events" and "Logs" sections to debug webhook delivery failures or billing errors.
