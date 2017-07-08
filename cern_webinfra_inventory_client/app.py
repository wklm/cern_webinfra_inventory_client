from inventory import Inventory, Model

import datetime
def main():
    instance_json = {
            "db_host": "test.cern.ch",
            "db_port": 8080,
            "db_user": "zbyszek",
            "db_password": "pass",
            "db_database": "db",
            "admin_egroup": "group",
            "enforce_SSO": True,
            "lb_name": "aaa",
            # "lb_ip": "23232323",
            "site_folder": "jeroijgoreijg",
            "drush_alias": "eriugjierug",
            "vhost_name": "geoirjgoierjg",
            "name": "ergkoeprkg",
            "full_domain": "rokgeropkg",
            "owner": "erokgpoerg",
            "administrators": "erogkoerpokg",
            "category": "erpokgreokg",
            "analytics": "reopkgporekg",
            "aliases": "orekgpoerkg",
            "type": "erkgpoerkgpoer",
            "creation_date": datetime.date(2001,7,7),
            "content_modification_date": datetime.date(2001,7,7),
            "expiration_date":  datetime.date(2001,7,7),
            "description": "eriufjhreiufh",
            "endpoint": "eferfre",
            "status": "qdqwd",
            "tn_enabled": True
    }

    Inventory().add_instance("drupal", instance_json)




if __name__ == '__main__':

    main()
