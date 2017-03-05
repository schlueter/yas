from yas.client import Client


def default_data_filter(yas_client, data):
    if data.get('type') not in yas_client.ignored_types \
            and 'channel' in data \
            and data.get('user') != yas_client.bot_id:
        channel = data['channel']
        channel_info = yas_client.api_call('channels.info', channel=channel)
        if channel_info.get('ok') and yas_client.at_bot in data['text']:
            return True
        group_info = yas_client.api_call('groups.info', channel=channel)
        if not channel_info.get('ok', False) and not group_info.get('ok', False):
            return True

def run():
    client = Client(data_filter=default_data_filter)
    client.listen()
