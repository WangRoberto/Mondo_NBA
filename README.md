# Mondo NBA
## Packages

| Name               | Version   |
|--------------------|-----------|
| asgiref            | 3.8.1     |
| certifi            | 2024.8.30 |
| charset-normalizer | 3.3.2     |
| Django             | 5.1       |
| idna               | 3.8       |
| pillow             | 10.4.0    |
| pip                | 24.1.2    |
| python-dotenv      | 1.0.1     |
| requests           | 2.32.3    |
| setuptools         | 71.1.0    |
| sqlparse           | 0.5.1     |
| stripe             | 10.9.0    |
| typing_extensions  | 4.12.2    |
| urllib3            | 2.2.2     |
| wheel              | 0.43.0    |

## Utilizzo
Dopo aver installato i vari pacchetti, 
si devono caricare nell'ambiente virtuale diverse variabili,
utilizzati durante la fase di pagamento, ovvero:
- STRIPE_SECRET_KEY_TEST
- STRIPE_PUBLIC_KEY_TEST
- STRIPE_WEBHOOK_SECRET_TEST
- PRODUCT_PRICE

Si usa il commando
'''console 
export
''' 
per caricarli nell'abiente virtuale.

Le variabili si ottengono dopo: 
- Essersi iscritti a "Stripe"
- Creato un prodotto
- Lanciato il seguente commando (serve per accettare le richieste di pagamento ed ottenere "STRIPE_WEBHOOK_SECRET_TEST"):
  - ./stripe listen --forward-to http://127.0.0.1:8000/gestione/stripe_webhook --api-key $STRIPE_SECRET_KEY_TEST
