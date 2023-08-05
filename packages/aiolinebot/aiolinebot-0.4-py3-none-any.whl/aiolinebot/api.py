"""aiolinebot.api module."""

import json

from linebot.api import LineBotApi
from linebot.http_client import HttpClient, RequestsHttpClient
from linebot.models import (
    Profile, MemberIds, Content, RichMenuResponse, MessageQuotaResponse,
    MessageQuotaConsumptionResponse, IssueLinkTokenResponse, IssueChannelTokenResponse,
    MessageDeliveryBroadcastResponse, MessageDeliveryMulticastResponse,
    MessageDeliveryPushResponse, MessageDeliveryReplyResponse,
    InsightMessageDeliveryResponse, InsightFollowersResponse, InsightDemographicResponse,
    InsightMessageEventResponse, BroadcastResponse, NarrowcastResponse,
    MessageProgressNarrowcastResponse,
)
from .http_client import AioHttpClient


class AioLineBotApi(LineBotApi):
    """AioLineBotApi provides asynchronous interface for LINE messaging API."""

    LINE_BOT_API_VERSION = '1.18.0'

    def __init__(self, channel_access_token,
                 endpoint=LineBotApi.DEFAULT_API_ENDPOINT,
                 data_endpoint=LineBotApi.DEFAULT_API_DATA_ENDPOINT,
                 timeout=HttpClient.DEFAULT_TIMEOUT,
                 http_client=RequestsHttpClient):
        """__init__ method.

        :param str channel_access_token: Your channel access token
        :param str endpoint: (optional) Default is https://api.line.me
        :param str data_endpoint: (optional) Default is https://api-data.line.me
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is linebot.http_client.HttpClient.DEFAULT_TIMEOUT
            If you set tuple, set float or other proper values
            for aiohttp_client.timeout after initialization.
        :type timeout: float | tuple(float, float)
        :param http_client: (optional) Default is
            :py:class:`linebot.http_client.RequestsHttpClient`
        :type http_client: T <= :py:class:`linebot.http_client.HttpClient`
        """
        super().__init__(channel_access_token, endpoint=endpoint, data_endpoint=data_endpoint,
                         timeout=timeout, http_client=http_client)

        self.aiohttp_client = AioHttpClient(timeout=timeout)

    async def broadcast_async(self, messages, retry_key=None, notification_disabled=False, timeout=None):
        """Call broadcast API.

        https://developers.line.biz/en/reference/messaging-api/#send-broadcast-message

        Sends push messages to multiple users at any time.

        :param messages: Messages.
            Max: 5
        :type messages: T <= :py:class:`linebot.models.send_messages.SendMessage` |
            list[T <= :py:class:`linebot.models.send_messages.SendMessage`]
        :param retry_key: (optional) Arbitrarily generated UUID in hexadecimal notation.
        :param bool notification_disabled: (optional) True to disable push notification
            when the message is sent. The default value is False.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.BroadcastResponse`
        """
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        if retry_key:
            self.headers['X-Line-Retry-Key'] = retry_key

        data = {
            'messages': [message.as_json_dict() for message in messages],
            'notificationDisabled': notification_disabled,
        }

        response = await self._post_async(
            '/v2/bot/message/broadcast', data=json.dumps(data), timeout=timeout
        )

        return BroadcastResponse(request_id=response.headers.get('X-Line-Request-Id'))

    async def cancel_default_rich_menu_async(self, timeout=None):
        """Cancel the default rich menu set with the Messaging API.

        https://developers.line.biz/en/reference/messaging-api/#cancel-default-rich-menu

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._delete_async(
            '/v2/bot/user/all/richmenu',
            timeout=timeout
        )

    async def create_rich_menu_async(self, rich_menu, timeout=None):
        """Call create rich menu API.

        https://developers.line.me/en/docs/messaging-api/reference/#create-rich-menu

        :param rich_menu: Inquired to create a rich menu object.
        :type rich_menu: T <= :py:class:`linebot.models.rich_menu.RichMenu`
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: str
        :return: rich menu id
        """
        response = await self._post_async(
            '/v2/bot/richmenu', data=rich_menu.as_json_string(), timeout=timeout
        )

        return response.json.get('richMenuId')

    async def delete_rich_menu_async(self, rich_menu_id, timeout=None):
        """Call delete rich menu API.

        https://developers.line.me/en/docs/messaging-api/reference/#delete-rich-menu

        :param str rich_menu_id: ID of an uploaded rich menu
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._delete_async(
            '/v2/bot/richmenu/{rich_menu_id}'.format(rich_menu_id=rich_menu_id),
            timeout=timeout
        )

    async def get_bot_info_async(self, timeout=None):
        """Get a bot's basic information.

        https://developers.line.biz/en/reference/messaging-api/#get-bot-info

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.BotInfo`
        """
        response = await self._get_async(
            '/v2/bot/info',
            timeout=timeout
        )

        return BotInfo.new_from_json_dict(response.json)

    async def get_default_rich_menu_async(self, timeout=None):
        """Get the ID of the default rich menu set with the Messaging API.

        https://developers.line.biz/en/reference/messaging-api/#get-default-rich-menu-id

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        response = await self._get_async(
            '/v2/bot/user/all/richmenu',
            timeout=timeout
        )

        return response.json.get('richMenuId')

    async def get_group_member_ids_async(self, group_id, start=None, timeout=None):
        """Call get group member IDs API.

        https://developers.line.biz/en/reference/messaging-api/#get-group-member-ids

        Gets the user IDs of the members of a group that the bot is in.
        This includes the user IDs of users who have not added the bot as a friend
        or has blocked the bot.

        :param str group_id: Group ID
        :param str start: continuationToken
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MemberIds`
        :return: MemberIds instance
        """
        params = None if start is None else {'start': start}

        response = await self._get_async(
            '/v2/bot/group/{group_id}/members/ids'.format(group_id=group_id),
            params=params,
            timeout=timeout
        )

        return MemberIds.new_from_json_dict(response.json)

    async def get_group_member_profile_async(self, group_id, user_id, timeout=None):
        """Call get group member profile API.

        https://developers.line.biz/en/reference/messaging-api/#get-group-member-profile

        Gets the user profile of a member of a group that
        the bot is in. This can be the user ID of a user who has
        not added the bot as a friend or has blocked the bot.

        :param str group_id: Group ID
        :param str user_id: User ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Profile`
        :return: Profile instance
        """
        response = await self._get_async(
            '/v2/bot/group/{group_id}/member/{user_id}'.format(group_id=group_id, user_id=user_id),
            timeout=timeout
        )

        return Profile.new_from_json_dict(response.json)

    async def get_group_members_count_async(self, group_id, timeout=None):
        """Call get members in group count API.

        https://developers.line.biz/en/reference/messaging-api/#get-members-group-count

        Gets the count of members in a group.

        :param str group_id: Group ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Group`
        :return: Profile instance
        """
        response = await self._get_async(
            '/v2/bot/group/{group_id}/members/count'.format(group_id=group_id),
            timeout=timeout
        )

        return response.json.get('count')

    async def get_group_summary_async(self, group_id, timeout=None):
        """Call get group summary API.

        https://developers.line.biz/en/reference/messaging-api/#get-group-summary

        Gets the group ID, group name, and group icon URL of a group
        where the LINE Official Account is a member.

        :param str group_id: Group ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Group`
        :return: Profile instance
        """
        response = await self._get_async(
            '/v2/bot/group/{group_id}/summary'.format(group_id=group_id),
            timeout=timeout
        )

        return Group.new_from_json_dict(response.json)

    async def get_insight_demographic_async(self, timeout=None):
        """Retrieve the demographic attributes for a bot's friends.

        https://developers.line.biz/en/reference/messaging-api/#get-demographic

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.InsightDemographicResponse`
        """
        response = await self._get_async(
            '/v2/bot/insight/demographic',
            timeout=timeout
        )

        return InsightDemographicResponse.new_from_json_dict(response.json)

    async def get_insight_followers_async(self, date, timeout=None):
        """Get the number of users who have added the bot on or before a specified date.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-followers

        :param str date: Date for which to retrieve the number of followers.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.InsightFollowersResponse`
        """
        response = await self._get_async(
            '/v2/bot/insight/followers?date={date}'.format(date=date),
            timeout=timeout
        )

        return InsightFollowersResponse.new_from_json_dict(response.json)

    async def get_insight_message_delivery_async(self, date, timeout=None):
        """Get the number of messages sent on a specified day.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-delivery-messages

        :param str date: Date for which to retrieve number of sent messages.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.InsightMessageDeliveryResponse`
        """
        response = await self._get_async(
            '/v2/bot/insight/message/delivery?date={date}'.format(date=date),
            timeout=timeout
        )

        return InsightMessageDeliveryResponse.new_from_json_dict(response.json)

    async def get_insight_message_event_async(self, request_id, timeout=None):
        """Return statistics about how users interact with broadcast messages.

        https://developers.line.biz/en/reference/messaging-api/#get-message-event

        :param str request_id: Request ID of broadcast message.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.InsightMessageEventResponse`
        """
        response = await self._get_async(
            '/v2/bot/insight/message/event?requestId={request_id}'.format(request_id=request_id),
            timeout=timeout
        )

        return InsightMessageEventResponse.new_from_json_dict(response.json)

    async def get_message_content_async(self, message_id, timeout=None):
        """Call get content API.

        https://developers.line.biz/en/reference/messaging-api/#get-content

        Retrieve image, video, and audio data sent by users.

        :param str message_id: Message ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Content`
        :return: Content instance
        """
        response = await self._get_async(
            '/v2/bot/message/{message_id}/content'.format(message_id=message_id),
            endpoint=self.data_endpoint, stream=True, timeout=timeout
        )

        return Content(response)

    async def get_message_delivery_broadcast_async(self, date, timeout=None):
        """Get number of sent broadcast messages.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-broadcast-messages

        Gets the number of messages sent with the /bot/message/broadcast endpoint.

        :param str date: Date the messages were sent. The format is `yyyyMMdd` (Timezone is UTC+9).
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MessageDeliveryBroadcastResponse`
        """
        response = await self._get_async(
            '/v2/bot/message/delivery/broadcast?date={date}'.format(date=date),
            timeout=timeout
        )

        return MessageDeliveryBroadcastResponse.new_from_json_dict(response.json)

    async def get_message_delivery_multicast_async(self, date, timeout=None):
        """Get number of sent multicast messages.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-multicast-messages

        Gets the number of messages sent with the /bot/message/multicast endpoint.

        :param str date: Date the messages were sent. The format is `yyyyMMdd` (Timezone is UTC+9).
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MessageDeliveryMulticastResponse`
        """
        response = await self._get_async(
            '/v2/bot/message/delivery/multicast?date={date}'.format(date=date),
            timeout=timeout
        )

        return MessageDeliveryMulticastResponse.new_from_json_dict(response.json)

    async def get_message_delivery_push_async(self, date, timeout=None):
        """Get number of sent push messages.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-push-messages

        Gets the number of messages sent with the /bot/message/push endpoint.

        :param str date: Date the messages were sent. The format is `yyyyMMdd` (Timezone is UTC+9).
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MessageDeliveryPushResponse`
        """
        response = await self._get_async(
            '/v2/bot/message/delivery/push?date={date}'.format(date=date),
            timeout=timeout
        )

        return MessageDeliveryPushResponse.new_from_json_dict(response.json)

    async def get_message_delivery_reply_async(self, date, timeout=None):
        """Get number of sent reply messages.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-reply-messages

        Gets the number of messages sent with the /bot/message/reply endpoint.

        :param str date: Date the messages were sent. The format is `yyyyMMdd` (Timezone is UTC+9).
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MessageDeliveryReplyResponse`
        """
        response = await self._get_async(
            '/v2/bot/message/delivery/reply?date={date}'.format(date=date),
            timeout=timeout
        )

        return MessageDeliveryReplyResponse.new_from_json_dict(response.json)

    async def get_message_quota_async(self, timeout=None):
        """Call Get the target limit for additional messages.

        https://developers.line.biz/en/reference/messaging-api/#get-quota

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MessageQuotaResponse`
        :return: MessageQuotaResponse instance
        """
        response = await self._get_async(
            '/v2/bot/message/quota',
            timeout=timeout
        )

        return MessageQuotaResponse.new_from_json_dict(response.json)

    async def get_message_quota_consumption_async(self, timeout=None):
        """Get number of messages sent this month.

        https://developers.line.biz/en/reference/messaging-api/#get-consumption

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MessageQuotaConsumptionResponse`
        :return: MessageQuotaConsumptionResponse instance
        """
        response = await self._get_async(
            '/v2/bot/message/quota/consumption',
            timeout=timeout
        )

        return MessageQuotaConsumptionResponse.new_from_json_dict(response.json)

    async def get_profile_async(self, user_id, timeout=None):
        """Call get profile API.

        https://developers.line.biz/en/reference/messaging-api/#get-profile

        Get user profile information.

        :param str user_id: User ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Profile`
        :return: Profile instance
        """
        response = await self._get_async(
            '/v2/bot/profile/{user_id}'.format(user_id=user_id),
            timeout=timeout
        )

        return Profile.new_from_json_dict(response.json)

    async def get_progress_status_narrowcast_async(self, request_id, timeout=None):
        """Get progress status of narrowcast messages sent.

        https://developers.line.biz/en/reference/messaging-api/#get-narrowcast-progress-status

        Gets the number of messages sent with the /bot/message/progress/narrowcast endpoint.

        :param str request_id: request ID of narrowcast.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MessageDeliveryBroadcastResponse`
        """
        response = await self._get_async(
            '/v2/bot/message/progress/narrowcast?requestId={request_id}'.format(
                request_id=request_id),
            timeout=timeout
        )

        return MessageProgressNarrowcastResponse.new_from_json_dict(response.json)

    async def get_rich_menu_async(self, rich_menu_id, timeout=None):
        """Call get rich menu API.

        https://developers.line.me/en/docs/messaging-api/reference/#get-rich-menu

        :param str rich_menu_id: ID of the rich menu
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.RichMenuResponse`
        :return: RichMenuResponse instance
        """
        response = await self._get_async(
            '/v2/bot/richmenu/{rich_menu_id}'.format(rich_menu_id=rich_menu_id),
            timeout=timeout
        )

        return RichMenuResponse.new_from_json_dict(response.json)

    async def get_rich_menu_id_of_user_async(self, user_id, timeout=None):
        """Call get rich menu ID of user API.

        https://developers.line.me/en/docs/messaging-api/reference/#get-rich-menu-id-of-user

        :param str user_id: IDs of the user
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: str
        :return: rich menu id
        """
        response = await self._get_async(
            '/v2/bot/user/{user_id}/richmenu'.format(user_id=user_id),
            timeout=timeout
        )

        return response.json.get('richMenuId')

    async def get_rich_menu_image_async(self, rich_menu_id, timeout=None):
        """Call download rich menu image API.

        https://developers.line.me/en/docs/messaging-api/reference/#download-rich-menu-image

        :param str rich_menu_id: ID of the rich menu with the image to be downloaded
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Content`
        :return: Content instance
        """
        response = await self._get_async(
            '/v2/bot/richmenu/{rich_menu_id}/content'.format(rich_menu_id=rich_menu_id),
            endpoint=self.data_endpoint, timeout=timeout
        )

        return Content(response)

    async def get_rich_menu_list_async(self, timeout=None):
        """Call get rich menu list API.

        https://developers.line.me/en/docs/messaging-api/reference/#get-rich-menu-list

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: list(T <= :py:class:`linebot.models.responses.RichMenuResponse`)
        :return: list[RichMenuResponse] instance
        """
        response = await self._get_async(
            '/v2/bot/richmenu/list',
            timeout=timeout
        )

        result = []
        for richmenu in response.json['richmenus']:
            result.append(RichMenuResponse.new_from_json_dict(richmenu))

        return result

    async def get_room_member_ids_async(self, room_id, start=None, timeout=None):
        """Call get room member IDs API.

        https://developers.line.biz/en/reference/messaging-api/#get-room-member-ids

        Gets the user IDs of the members of a group that the bot is in.
        This includes the user IDs of users who have not added the bot as a friend
        or has blocked the bot.

        :param str room_id: Room ID
        :param str start: continuationToken
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MemberIds`
        :return: MemberIds instance
        """
        params = None if start is None else {'start': start}

        response = await self._get_async(
            '/v2/bot/room/{room_id}/members/ids'.format(room_id=room_id),
            params=params,
            timeout=timeout
        )

        return MemberIds.new_from_json_dict(response.json)

    async def get_room_member_profile_async(self, room_id, user_id, timeout=None):
        """Call get room member profile API.

        https://developers.line.biz/en/reference/messaging-api/#get-room-member-profile

        Gets the user profile of a member of a room that
        the bot is in. This can be the user ID of a user who has
        not added the bot as a friend or has blocked the bot.

        :param str room_id: Room ID
        :param str user_id: User ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Profile`
        :return: Profile instance
        """
        response = await self._get_async(
            '/v2/bot/room/{room_id}/member/{user_id}'.format(room_id=room_id, user_id=user_id),
            timeout=timeout
        )

        return Profile.new_from_json_dict(response.json)

    async def get_room_members_count_async(self, room_id, timeout=None):
        """Call get members in room count API.

        https://developers.line.biz/en/reference/messaging-api/#get-members-room-count

        Gets the count of members in a room.

        :param str room_id: Room ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Group`
        :return: Profile instance
        """
        response = await self._get_async(
            '/v2/bot/room/{room_id}/members/count'.format(room_id=room_id),
            timeout=timeout
        )

        return response.json.get('count')

    async def get_webhook_endpoint_async(self, timeout=None):
        """Get information on a webhook endpoint.

        https://developers.line.biz/en/reference/messaging-api/#get-webhook-endpoint-information

        :rtype: :py:class:`linebot.models.responses.GetWebhookResponse`
        :return: Webhook information, including `endpoint` for webhook
            URL and `active` for webhook usage status.
        """
        response = await self._get_async(
            '/v2/bot/channel/webhook/endpoint',
            timeout=timeout,
        )

        return GetWebhookResponse.new_from_json_dict(response.json)

    async def issue_channel_token_async(self, client_id, client_secret,
                            grant_type='client_credentials', timeout=None):
        """Issues a short-lived channel access token.

        https://developers.line.biz/en/reference/messaging-api/#issue-channel-access-token

        :param str client_id: Channel ID.
        :param str client_secret: Channel secret.
        :param str grant_type: `client_credentials`
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.IssueChannelTokenResponse`
        :return: IssueChannelTokenResponse instance
        """
        response = await self._post_async(
            '/v2/oauth/accessToken',
            data={
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': grant_type,
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=timeout
        )

        return IssueChannelTokenResponse.new_from_json_dict(response.json)

    async def issue_link_token_async(self, user_id, timeout=None):
        """Issues a link token used for the account link feature.

        https://developers.line.biz/en/reference/messaging-api/#issue-link-token

        :param str user_id: User ID for the LINE account to be linked
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.IssueLinkTokenResponse`
        :return: IssueLinkTokenResponse instance
        """
        response = await self._post_async(
            '/v2/bot/user/{user_id}/linkToken'.format(
                user_id=user_id
            ),
            timeout=timeout
        )

        return IssueLinkTokenResponse.new_from_json_dict(response.json)

    async def leave_group_async(self, group_id, timeout=None):
        """Call leave group API.

        https://developers.line.biz/en/reference/messaging-api/#leave-group

        Leave a group.

        :param str group_id: Group ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post_async(
            '/v2/bot/group/{group_id}/leave'.format(group_id=group_id),
            timeout=timeout
        )

    async def leave_room_async(self, room_id, timeout=None):
        """Call leave room API.

        https://developers.line.biz/en/reference/messaging-api/#leave-room

        Leave a room.

        :param str room_id: Room ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post_async(
            '/v2/bot/room/{room_id}/leave'.format(room_id=room_id),
            timeout=timeout
        )

    async def link_rich_menu_to_user_async(self, user_id, rich_menu_id, timeout=None):
        """Call link rich menu to user API.

        https://developers.line.me/en/docs/messaging-api/reference/#link-rich-menu-to-user

        :param str user_id: ID of the user
        :param str rich_menu_id: ID of an uploaded rich menu
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post_async(
            '/v2/bot/user/{user_id}/richmenu/{rich_menu_id}'.format(
                user_id=user_id,
                rich_menu_id=rich_menu_id
            ),
            timeout=timeout
        )

    async def link_rich_menu_to_users_async(self, user_ids, rich_menu_id, timeout=None):
        """Links a rich menu to multiple users.

        https://developers.line.biz/en/reference/messaging-api/#link-rich-menu-to-users

        :param user_ids: user IDs
            Max: 150 users
        :type user_ids: list[str]
        :param str rich_menu_id: ID of an uploaded rich menu
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post_async(
            '/v2/bot/richmenu/bulk/link',
            data=json.dumps({
                'userIds': user_ids,
                'richMenuId': rich_menu_id,
            }),
            timeout=timeout
        )

    async def multicast_async(self, to, messages, retry_key=None, notification_disabled=False, timeout=None):
        """Call multicast API.

        https://developers.line.biz/en/reference/messaging-api/#send-multicast-message

        Sends push messages to multiple users at any time.
        Messages cannot be sent to groups or rooms.

        :param to: IDs of the receivers
            Max: 150 users
        :type to: list[str]
        :param messages: Messages.
            Max: 5
        :type messages: T <= :py:class:`linebot.models.send_messages.SendMessage` |
            list[T <= :py:class:`linebot.models.send_messages.SendMessage`]
        :param retry_key: (optional) Arbitrarily generated UUID in hexadecimal notation.
        :param bool notification_disabled: (optional) True to disable push notification
            when the message is sent. The default value is False.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        if retry_key:
            self.headers['X-Line-Retry-Key'] = retry_key

        data = {
            'to': to,
            'messages': [message.as_json_dict() for message in messages],
            'notificationDisabled': notification_disabled,
        }

        await self._post_async(
            '/v2/bot/message/multicast', data=json.dumps(data), timeout=timeout
        )

    async def narrowcast_async(
            self, messages,
            retry_key=None, recipient=None, filter=None, limit=None,
            notification_disabled=False, timeout=None):
        """Call narrowcast API.

        https://developers.line.biz/en/reference/messaging-api/#send-narrowcast-message

        Sends push messages to multiple users at any time.
        Messages cannot be sent to groups or rooms.

        :param messages: Messages.
            Max: 5
        :type messages: T <= :py:class:`linebot.models.send_messages.SendMessage` |
            list[T <= :py:class:`linebot.models.send_messages.SendMessage`]
        :param retry_key: (optional) Arbitrarily generated UUID in hexadecimal notation.
        :param recipient: audience object of recipient
        :type recipient: T <= :py:class:`linebot.models.recipient.AudienceRecipient`
        :param filter: demographic filter of recipient
        :type filter: T <= :py:class:`linebot.models.filter.DemographicFilter`
        :param limit: limit on this narrowcast
        :type limit: T <= :py:class:`linebot.models.limit.Limit`
        :param bool notification_disabled: (optional) True to disable push notification
            when the message is sent. The default value is False.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.NarrowcastResponse`
        """
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        if retry_key:
            self.headers['X-Line-Retry-Key'] = retry_key

        data = {
            'messages': [message.as_json_dict() for message in messages],
            'recipient': recipient.as_json_dict(),
            'filter': filter.as_json_dict(),
            'limit': limit.as_json_dict(),
            'notificationDisabled': notification_disabled,
        }

        response = await self._post_async(
            '/v2/bot/message/narrowcast', data=json.dumps(data), timeout=timeout
        )

        return NarrowcastResponse(request_id=response.headers.get('X-Line-Request-Id'))

    async def push_message_async(
            self, to, messages,
            retry_key=None, notification_disabled=False, timeout=None):
        """Call push message API.

        https://developers.line.biz/en/reference/messaging-api/#send-push-message

        Send messages to users, groups, and rooms at any time.

        :param str to: ID of the receiver
        :param messages: Messages.
            Max: 5
        :type messages: T <= :py:class:`linebot.models.send_messages.SendMessage` |
            list[T <= :py:class:`linebot.models.send_messages.SendMessage`]
        :param retry_key: (optional) Arbitrarily generated UUID in hexadecimal notation.
        :param bool notification_disabled: (optional) True to disable push notification
            when the message is sent. The default value is False.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        if retry_key:
            self.headers['X-Line-Retry-Key'] = retry_key

        data = {
            'to': to,
            'messages': [message.as_json_dict() for message in messages],
            'notificationDisabled': notification_disabled,
        }

        await self._post_async(
            '/v2/bot/message/push', data=json.dumps(data), timeout=timeout
        )

    async def reply_message_async(self, reply_token, messages, notification_disabled=False, timeout=None):
        """Call reply message API.

        https://developers.line.biz/en/reference/messaging-api/#send-reply-message

        Respond to events from users, groups, and rooms.

        Webhooks are used to notify you when an event occurs.
        For events that you can respond to, a replyToken is issued for replying to messages.

        Because the replyToken becomes invalid after a certain period of time,
        responses should be sent as soon as a message is received.

        Reply tokens can only be used once.

        :param str reply_token: replyToken received via webhook
        :param messages: Messages.
            Max: 5
        :type messages: T <= :py:class:`linebot.models.send_messages.SendMessage` |
            list[T <= :py:class:`linebot.models.send_messages.SendMessage`]
        :param bool notification_disabled: (optional) True to disable push notification
            when the message is sent. The default value is False.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        data = {
            'replyToken': reply_token,
            'messages': [message.as_json_dict() for message in messages],
            'notificationDisabled': notification_disabled,
        }

        await self._post_async(
            '/v2/bot/message/reply', data=json.dumps(data), timeout=timeout
        )

    async def revoke_channel_token_async(self, access_token, timeout=None):
        """Revokes a channel access token.

        https://developers.line.biz/en/reference/messaging-api/#revoke-channel-access-token

        :param str access_token: Channel access token.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post_async(
            '/v2/oauth/revoke',
            data={'access_token': access_token},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=timeout
        )

    async def set_default_rich_menu_async(self, rich_menu_id, timeout=None):
        """Set the default rich menu.

        https://developers.line.biz/en/reference/messaging-api/#set-default-rich-menu

        :param str rich_menu_id: ID of an uploaded rich menu
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post_async(
            '/v2/bot/user/all/richmenu/{rich_menu_id}'.format(
                rich_menu_id=rich_menu_id,
            ),
            timeout=timeout
        )

    async def set_rich_menu_image_async(self, rich_menu_id, content_type, content, timeout=None):
        """Call upload rich menu image API.

        https://developers.line.me/en/docs/messaging-api/reference/#upload-rich-menu-image

        Uploads and attaches an image to a rich menu.

        :param str rich_menu_id: IDs of the richmenu
        :param str content_type: image/jpeg or image/png
        :param content: image content as bytes, or file-like object
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post_async(
            '/v2/bot/richmenu/{rich_menu_id}/content'.format(rich_menu_id=rich_menu_id),
            endpoint=self.data_endpoint,
            data=content,
            headers={'Content-Type': content_type},
            timeout=timeout
        )

    async def set_webhook_endpoint_async(self, webhook_endpoint, timeout=None):
        """Set the webhook endpoint URL.

        https://developers.line.biz/en/reference/messaging-api/#set-webhook-endpoint-url

        :param str webhook_endpoint: A valid webhook URL to be set.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: dict
        :return: Empty dict.
        """
        data = {
            'endpoint': webhook_endpoint
        }

        response = self._put(
            '/v2/bot/channel/webhook/endpoint',
            data=json.dumps(data),
            timeout=timeout,
        )

        return response.json

    async def test_webhook_endpoint_async(self, webhook_endpoint=None, timeout=None):
        """Checks if the configured webhook endpoint can receive a test webhook event.

        https://developers.line.biz/en/reference/messaging-api/#test-webhook-endpoint

        :param webhook_endpoint: (optional) Set this parameter to
            specific the webhook endpoint of the webhook. Default is the webhook
            endpoint that is already set to the channel.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.TestWebhookResponse`
        """
        data = {}

        if webhook_endpoint is not None:
            data['endpoint'] = webhook_endpoint

        response = await self._post_async(
            '/v2/bot/channel/webhook/test',
            data=json.dumps(data),
            timeout=timeout,
        )

        return TestWebhookResponse.new_from_json_dict(response.json)

    async def unlink_rich_menu_from_user_async(self, user_id, timeout=None):
        """Call unlink rich menu from user API.

        https://developers.line.me/en/docs/messaging-api/reference/#unlink-rich-menu-from-user

        :param str user_id: ID of the user
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._delete_async(
            '/v2/bot/user/{user_id}/richmenu'.format(user_id=user_id),
            timeout=timeout
        )

    async def unlink_rich_menu_from_users_async(self, user_ids, timeout=None):
        """Unlinks rich menus from multiple users.

        https://developers.line.biz/en/reference/messaging-api/#unlink-rich-menu-from-users

        :param user_ids: user IDs
            Max: 150 users
        :type user_ids: list[str]
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post_async(
            '/v2/bot/richmenu/bulk/unlink',
            data=json.dumps({
                'userIds': user_ids,
            }),
            timeout=timeout
        )

    async def _get_async(self, path, endpoint=None, params=None, headers=None, stream=False, timeout=None):
        url = (endpoint or self.endpoint) + path

        if headers is None:
            headers = {}
        headers.update(self.headers)

        response = await self.aiohttp_client.get(
            url, headers=headers, params=params, stream=stream, timeout=timeout
        )

        response.check_error()
        return response

    async def _post_async(self, path, endpoint=None, data=None, headers=None, timeout=None):
        url = (endpoint or self.endpoint) + path

        if headers is None:
            headers = {'Content-Type': 'application/json'}
        headers.update(self.headers)

        response = await self.aiohttp_client.post(
            url, headers=headers, data=data, timeout=timeout
        )

        response.check_error()
        return response

    async def _delete_async(self, path, endpoint=None, data=None, headers=None, timeout=None):
        url = (endpoint or self.endpoint) + path

        if headers is None:
            headers = {}
        headers.update(self.headers)

        response = await self.aiohttp_client.delete(
            url, headers=headers, data=data, timeout=timeout
        )

        response.check_error()
        return response
