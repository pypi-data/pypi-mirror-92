# Test data for ISCC


## Installation

```console
$ pip install iscc-samples
```

## Usage:
```python
import iscc_samples as samples

for path in samples.videos():
    print(path)
```

## Development

### Making a release

```console
$ poetry build -f sdist
$ poetry publish
```


## Maintainers

[@titusz](https://github.com/titusz)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

You may also want join our developer chat on Telegram at <https://t.me/iscc_dev>.


## Change Log

### [0.1.0] - 2019-05-31

- Initial release with basic sample files

## License

CC-BY-4.0 © 2021 Titusz Pan
