# To Personalise or Not? Why Personalisation Knowledge Can Fall Short in Enhancing Conversational Information Seeking

Official repository for the paper "To Personalise or Not? Why Personalisation Knowledge Can Fall Short in Enhancing Conversational Information Seeking" (KEIR @ ECIR 2025).

This repository contains our new Personal Text Knowledge Base (PTKB) statement annotations for the TREC iKAT 2023 test collection. Our new human annotations allow us to specifically evaluate the effectiveness of personalised query reformulation (PQR).

To get the classification labels used in our paper and compute the Fleiss' Kappa:
```bash
$ conda create --name pqr python==3.10.13
$ conda activate pqr
$ pip install -r requirements.txt
$ python preprocessing_annotation.py
```