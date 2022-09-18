import toml
import client as client


print('Loading config...')
with open('config.toml', 'r') as f:
    config = toml.load(f)

if __name__ == '__main__':
    kagameshi = client.KagameshiBot(token=config['token'])
    kagameshi.run()
