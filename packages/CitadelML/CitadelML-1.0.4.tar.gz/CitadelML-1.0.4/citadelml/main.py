import requests
import json


# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# upload_model('http://localhost:5000', 'example_dataset', 'jdoe1', 'secret', 'model', 'loss', 'adam')

def upload_model(
        server: str,
        dataset: str,
        username: str,
        password: str,
        model,
        loss_function,
        optimizer: str,
        n_epochs: int = 5,
        seed: int = 123,
        split: float = 0.2,
        batch_size: int = 32,
        save_training_results: bool = False
):

    """
    Upload a Tensorflow2 model to server
    :param server: URL of server
    :param dataset: Dataset training will be done on
    :param username: Account username on server
    :param password: Account password on server
    :param model: Tensorflow model object
    :param loss_function: Tensorflow loss function
    :param optimizer: Tensorflow optimizer, as string
    :param n_epochs: Number of epochs for training
    :param seed: Random seed for dataset split
    :param split: Train/Validation split amount
    :param batch_size: Dataset batch size
    :param save_training_results Whether to save the output of the model to the server. Note: Only admins may view actual weights
    :return: Training ID
    """

    # Ensure server is running
    try:
        requests.get(server)
    except ConnectionError:
        raise ValueError('Unable to connect to server. Ensure the URL is correct and that the server is running.')

    # Obtain authentication token for server
    response = requests.post(server+'/auth/login', data={
        'username': username,
        'password': password
    })

    if 'access_token' not in response.json():
        raise ValueError('Unable to log in to server. Invalid username or password specified.')

    access_token = response.json()['access_token']

    # Convert model structure to JSON
    model_json = model.to_json()

    request_headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer ' + access_token
    }

    request_body = {
        'model_structure': model_json,
        'optimizer': optimizer,
        'loss_function': "TODO: Implement Dynamic Loss Functions",
        'n_epochs': n_epochs,
        'dataset': dataset,
        'seed': seed,
        'split': split,
        'batch_size': batch_size,
        'save_training_results': save_training_results
    }

    response = requests.post(server+'/training/train', headers=request_headers, data=json.dumps(request_body))

    if 'training_id' not in response.json():
        raise ValueError('Unable to send training data to server. Ensure your account has sufficient permissions.')

    return response.json()['training_id']
