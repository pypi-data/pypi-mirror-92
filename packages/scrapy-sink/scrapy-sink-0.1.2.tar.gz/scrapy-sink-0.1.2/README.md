# Pipeline to post scrapy item to your url


## Installation

Install scrapy-sink using pip::

    $ pip install scrapy-sink

## Configuration

1. Add the  ``settings.py`` of your Scrapy project like this:

```python
SINK_ADDR = 'http://127.0.0.1:8000/data_receiver.php'
```

You can also only set it in your environment variable

2. Enable the pipeline by adding it to ``ITEM_PIPELINES`` in your ``settings.py`` file and changing HttpCompressionMiddleware
 priority:
   
```python
ITEM_PIPELINES = {
    'scrapy_sink.pipelines.SinkPipeline': 9999,
}
```
The order should after your persist pipeline such as save to database and after your preprocess pipeline.

## Usage

no need to change your code

## Getting help

Please use github issue

## Contributing

PRs are always welcomed.