from pyyoutube import Api
from pyyoutube.models import AccessToken
import ast

# Cloud project: https://console.cloud.google.com/apis/credentials/consent/edit;newAppInternalUser=false?project=govhack21

# Make these a build flag.
NEEDS_ACCESS = False
NEEDS_TOKEN_OVERRIDE = False

def create_api():
	
	with open('secret_keys.txt', 'r') as fh:
		contents = fh.read()
		key_data = ast.literal_eval(contents)

	# return
	if NEEDS_ACCESS:
		# This process is kinda munted.
		api = Api(client_id=key_data["youtube_oauth_client_id"], client_secret=key_data["youtube_oauth_client_secret"])
		print(api.get_authorization_url())
		if key_data["youtube_oauth_full"] and not NEEDS_TOKEN_OVERRIDE:
			access_token = api.generate_access_token(
				authorization_response=key_data["youtube_oauth_full"]
			)
			
			token = {
				"access_token": access_token.access_token,
				"expires_in": access_token.expires_in,
				"refresh_token": access_token.refresh_token,
				"scope": access_token.scope,
				"token_type": access_token.token_type,
				"id_token": access_token.id_token,

			}
			with open('token_dump', 'w') as fh:
				fh.write(str(token))
			# TODO: Fix up flow.
		else:
			# Carry out oauth flow nad update secrets.
			raise Error("Something something oauth flow & token broken")
	else:
		# Non user API.
		api = Api(api_key=key_data["youtube_api_key"])
	return api


def main():
	api = create_api()
	channels_liked = api.get_subscription_by_channel(channel_id="UCxB9nqYZLVvo0zX8qjhQmsg",
		parts="id,snippet",
		count=350 
	)

	liked_topics = set()

	channel_data_corpus = []

	for channel in channels_liked.items:
		channel_id = channel.snippet.resourceId.channelId
		channel_info = api.get_channel_info(channel_id=channel_id)
		try:
			channel_topics = channel_info.items[0].to_dict()["topicDetails"]["topicCategories"]
			channel_sentance = channel_info.items[0].to_dict()['snippet']['title'] + channel_info.items[0].to_dict()['snippet']['description']


			for topic in channel_topics:
				liked_topics.add(topic)
				channel_sentance += topic + " "

			channel_data_corpus.append(channel_sentance)

		except:
			print("Failed to get topics for: " + str(channel))

	print(liked_topics)
	with open('liked_topics', 'w') as fh:
		fh.write(str(liked_topics))

	with open('channel_data_corpus', 'w') as fh:
		fh.writelines(channel_data_corpus)

main()
