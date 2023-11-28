# Red Search

## Getting started

- add your `resources/secrets.yaml` file with your API keys for YouTube.

```yaml
- name: youtube
  api_key: <your key>
```

## Commands

- [X] `python run.py --help` for help
- [X] `python run.py scrap channels resources/urls.txt resources/channels.yaml` to build the database of channels from a list of URLs in the file `resources/urls.txt`
- [ ] `python run.py scrap transcriptions resources/channels.yaml resources/index.yaml` to get all videos and transcriptions from channels in the file `resources/channels.yaml` and build the first index
- [ ] `python run.py process topic resources/index.yaml` to process the transcriptions in the index and build the topic model
- [ ] `python run.py process topic-timeline resources/index.yaml` to process the transcriptions in the index and build the topic model with a timeline
- [ ] `python run.py process cross-reference resources/index.yaml` to process the transcriptions in the index and build the cross-reference with other channels/videos
- [ ] `python run.py process cortes resources/index.yaml` to process the transcriptions in the index and build automatic cuts


