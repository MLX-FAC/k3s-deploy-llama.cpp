# Deploy Lora Model

<img src="https://cdn.mlx.institute/assets/MLX4.4_-_Deploying_a_Model_with_K3.avif">

## Step 0 - Prerequisites
Go to your server and install k3s
```bash
curl -sfL https://get.k3s.io | sh -
```

## Step 1 - Update the env variables
Copy the deploy.yaml to the server, and update it with your details
> deploy.yaml
```yaml
name: HF_TOKEN
value: <Your Token>
name: LORA_REPO
value: <Your Repo>
```

## Step 2 - Apply the deploy.yaml manifest
While on the server, apply the deploy.yaml manifest
```bash
sudo kubectl apply -f deploy.yaml
```

That's it
