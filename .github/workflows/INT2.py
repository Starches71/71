
name: Generate WireGuard Keys

on: 
  push:
    branches:
      - main  # Change this to the branch you want

jobs:
  generate-keys:
    runs-on: ubuntu-latest

    steps:
      - name: Install WireGuard
        run: |
          sudo apt update
          sudo apt install -y wireguard

      - name: Generate WireGuard Private and Public Keys
        run: |
          wg genkey | tee server_private_key | wg pubkey > server_public_key
          echo "Server Private Key:"
          cat server_private_key
          echo "Server Public Key:"
          cat server_public_key
