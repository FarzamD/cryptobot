# CryptoBot

<!-- ![Subway](./TehranSubway.PNG)   -->

## Introduction

* Providing a machine predicting best short long-time profiting crypto currency  
* Should also work for stock

## Data

* Data consists of two parts:

1. Dependent variables:

    * prices for last 30 days including max, min, average, open, and close (shape: (30,5))
    * prices for last day including max, min, average, open, and close for each hour(shape: (24,5))

2. Independent variables
  
    * 7-day profit
    * 7-day profit classified

## Models

* Eeach model folder represents a different type of model with distinctively different structure

* Each model is trained to find the optimized parameters