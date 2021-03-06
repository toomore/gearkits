''' Mattermost '''
# pylint: disable=arguments-renamed,arguments-differ
import logging
from typing import Any, Generator, Optional

from requests import Response, Session


class Mattermost(Session):
    ''' Mattermost '''

    def __init__(self, token: str, base_url: str, log_name: str = 'Mattermost'):
        super().__init__()
        self.token = token
        self.base_url = base_url
        self.log = logging.getLogger(log_name)
        self.headers.update({'Authorization': f'Bearer {self.token}'})

    def log_rate_limit(self, headers: dict[str, Any]) -> None:
        ''' Get log info from headers '''
        self.log.info('X-Ratelimit-Limit: %s, X-Ratelimit-Remaining: %s, X-Ratelimit-Reset: %s',
                      headers.get('X-Ratelimit-Limit'),
                      headers.get('X-Ratelimit-Remaining'),
                      headers.get('X-Ratelimit-Reset'),
                      )

    def get_users(self, page: int, per_page: int = 200) -> Response:
        ''' Get users '''
        return self.get(f'{self.base_url}/users', params={'page': page, 'per_page': per_page})

    def get_users_loop(self, per_page: int = 200) -> Generator[dict[str, Any], None, None]:
        ''' Get users in loop '''
        page = 0
        num = 0
        for user in self.get_users(page=page, per_page=per_page).json():
            yield user
            num += 1

        while num == per_page:
            page += 1
            num = 0
            for user in self.get_users(page=page, per_page=per_page).json():
                yield user
                num += 1

    def get_users_stats(self) -> Response:
        ''' Get users stats '''
        return self.get(f'{self.base_url}/users/stats')

    def get_user_by_username(self, username: str) -> Response:
        ''' Get user by username '''
        return self.get(f'{self.base_url}/users/username/{username}')

    def create_a_direct_message(self, users: str) -> Response:
        ''' Create a direct messge '''
        return self.post(f'{self.base_url}/channels/direct', json=users)

    def posts(self, channel_id: str, message: str) -> Response:
        ''' Posts message '''
        return self.post(f'{self.base_url}/posts',
                         json={'channel_id': channel_id, 'message': message})

    def get_posts_from_channel(self, channel_id: str) -> Response:
        ''' Get post from channel '''
        return self.get(f'{self.base_url}/channels/{channel_id}/posts')

    def post_invite_by_email(self, team_id: str, emails: list[str]) -> Response:
        ''' Post an invite by email '''
        return self.post(f'{self.base_url}/teams/{team_id}/invite/email', json=emails)

    def post_invite_guests_by_email(self, team_id: str, emails: list[str],
                                    channels: list[str], message: Optional[str] = None) -> Response:
        ''' Post an invite to guest by email '''
        data: dict[str, Any] = {
            'emails': emails,
            'channels': channels,
        }
        if message:
            data['message'] = message.strip()

        return self.post(f'{self.base_url}/teams/{team_id}/invite-guests/email', json=data)

    def post_user_to_channel(self, channel_id: str, uid: str) -> Response:
        ''' Post user to channel '''
        return self.post(f'{self.base_url}/channels/{channel_id}/members', json={'user_id': uid})

    def put_users_patch(self, uid: str, position: str) -> Response:
        ''' Update user '''
        data = {
            'position': position,
        }
        return self.put(f'{self.base_url}/users/{uid}/patch', json=data)
