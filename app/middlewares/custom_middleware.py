from django.core.exceptions import MiddlewareNotUsed
import logging
from app.libs.myCrypt import get_decrypt_data,get_encrypt_data
from api.settings import common as common_settings


class ApiMiddleware:
    logger = logging.getLogger('LogginApiMiddleware')

    def __init__(self, get_response):
        # raise MiddlewareNotUsed
        self.get_response = get_response
        print("ここ")

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

            # if 'user_id' in request.POST:
            #     # user_id = get_encrypt_data(request.GET['user_id'], common_settings.CRYPT_KEY, common_settings.CRYPT_IV).decode('utf-8')
            #     request.GET = request.GET.copy()
            #     request.GET['user_id'] = request.POST['user_id']

            if 'user_id' in request.GET:
                if request.path == '/users/exists/':
                    hash_user_id = get_encrypt_data(request.GET['user_id'], common_settings.CRYPT_KEY, common_settings.CRYPT_IV).decode('utf-8')
                    request.GET = request.GET.copy()
                    request.GET['user_id'] = hash_user_id

            if 'user_id' in request.POST:
                if request.path == '/users/register/':
                    post_usr_id = request.POST['user_id']
                    hasu_user_id = get_encrypt_data(post_usr_id, common_settings.CRYPT_KEY, common_settings.CRYPT_IV).decode('utf-8')
                    request.POST = request.POST.copy()
                    request.POST['user_id'] = hasu_user_id
                    request.POST['auth_id'] = post_usr_id
                # else :
                #     post_usr_id = request.POST['user_id']
                #     decript_user_id = get_decrypt_data(post_usr_id, common_settings.CRYPT_KEY, common_settings.CRYPT_IV).decode('utf-8')
                #     request.POST = request.POST.copy()
                #     request.POST['user_id'] = decript_user_id
                #     request.POST['auth_id'] = post_usr_id


        # フロントからはuser_idは暗号化されてくるので、ここで一括で複合化する
        self.logger.info('REMOTE_ADDR={}'.format(ip))
        response = self.get_response(request)
        print(response.content)
        response['Access-Control-Allow-Origin'] = 'http://localhost:1234'

        return response
