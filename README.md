# Invisible QR watermark

A python script that allows to encode a secret message/url/test to Image as a QR watermark, that is invisible to user's eyes

## Instalation

```
$ pip install invisible_qr_watermark
```

## Usage

Import library

```python
from invisible_qr_watermark import image
```

Create a new QRImage instance

```python
new_img = QRImage("path_to_img/img.jpg")
```

To encode use encode() method. Note that encode return PIL.Image.Image instance that can be stored as an image using save()

```python
encoded_img = new_img.encode("text I want to encode")
encoded_img.save("new_img.jpg")
```

To decode image use decode() method

```python
new_img.decode()
```

Output

```
$ 'text I want to encode'
```

## Tests

```
$ pytest
```
