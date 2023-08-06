## Pynovaposhta - NovaPoshta client for humans


### Installation

```shell
>>> pip install pynovaposhta
```


### Using

```python
from novaposhta import Novaposhta

client = Novaposhta(api_key='<YOUR_API_KEY>')

# Each model in NovaPoshta API has a corresponding client method
areas = client.addresses().get_areas()
```

### Supported models

- [x] [Addresses](https://devcenter.novaposhta.ua/docs/services/556d7ccaa0fe4f08e8f7ce43/operations/58e5ebeceea27017bc851d67)
- [x] [Counterparties](https://devcenter.novaposhta.ua/docs/services/557eb8c8a0fe4f02fc455b2d/operations/557fdcb4a0fe4f105c087611)
- [ ] [Printing](https://devcenter.novaposhta.ua/docs/services/556d7280a0fe4f08e8f7ce40/operations/557ed645a0fe4f02fc455b31)
- [ ] [ScanSheets](https://devcenter.novaposhta.ua/docs/services/55662bd3a0fe4f10086ec96e/operations/556c4786a0fe4f0634657b65)
- [ ] [Common](https://devcenter.novaposhta.ua/docs/services/55702570a0fe4f0cf4fc53ed/operations/55702571a0fe4f0b6483890f)
- [ ] [AdditionalService](https://devcenter.novaposhta.ua/docs/services/58ad7185eea27006cc36d649/operations/58b6b830ff2c200cd80adb91)
- [ ] [AdditionalServiceGeneral](https://devcenter.novaposhta.ua/docs/services/58f722b3ff2c200c04673bd1/operations/58f7233eff2c200c04673bd2)
- [ ] [InternetDocument](https://devcenter.novaposhta.ua/docs/services/556eef34a0fe4f02049c664e/operations/557eb417a0fe4f02fc455b2c)


### TODO:
- [ ] Supporting all models 
- [ ] Async version 
- [ ] Verbose documentation 
