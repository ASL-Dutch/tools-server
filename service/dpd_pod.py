# -*- coding:utf-8 -*-
import json
import logging
import traceback
import none as none
from util.account import account
from util.http_client import get_request, get_cookie_of_dpd, download_file_url_to_path

pod_url = 'https://tracking.dpd.de/rest/plc/en_EN/TRACKING_NO'
log_in_uri = 'https://tracking.dpd.de/login'


class DpdPod:
    def __init__(self, data, logger, save_path):
        """

        :param data:
        :param log:
        :param save_path:
        """
        self.data = data
        self.log = logger
        self.save_path = save_path

    def pull_pod(self):
        data, log = self.data, self.log
        count = 0

        for tracking_no in data:

            if not str(tracking_no).startswith('0'):
                tracking_no = '0' + str(tracking_no)
            else:
                tracking_no = str(tracking_no)

            url = pod_url.replace('TRACKING_NO', tracking_no)
            res = get_request(url)
            print(tracking_no + ':' + res)

            if res is not none:
                try:
                    js = json.loads(res)
                    link = self.get_dpd_pod_link(js)
                    print(link)
                    if link is not None:
                        d_res = self.download_pod(link, tracking_no)
                        if d_res:
                            count += 1
                        else:
                            log.error("%s has link but cannot download" % tracking_no)
                            log.error("%s link: %s" % (tracking_no, link))
                    else:
                        log.error("%s can not get pod link" % tracking_no)
                except:
                    log.error("%s can not get pod link" % tracking_no)
                    log.error(traceback.format_exc())
                    pass
            else:
                log.error("%s request dpd failed" % str(tracking_no))
        return count

    def get_dpd_pod_link(self, js):
        log = self.log
        try:
            scan_list = js['parcellifecycleResponse']['parcelLifeCycleData']['scanInfo']['scan']
            for s in scan_list:
                links = s['links']
                print("links:", links)
                if links is not None and len(links) > 0:
                    return links[0]['url']
        except:
            log.error("DPD cant parse scanInfo, response: %s" % js)
            log.error(traceback.format_exc())
            pass

    def download_pod(self, link, tracking_no):
        ups, dpd = account()
        cookie = get_cookie_of_dpd(log_in_uri, json.dumps(dpd))
        return download_file_url_to_path(link, cookie, self.save_path, tracking_no)


if __name__ == '__main__':
    dpd = DpdPod(['84150000286036'], logging.Logger, 'C:\\Users\\14917\\Desktop\\')
    dpd.pull_pod()
