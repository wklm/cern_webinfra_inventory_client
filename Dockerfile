FROM python

ADD . /cern_webinfra_inventory_client

WORKDIR /cern_webinfra_inventory_client

RUN pip install --upgrade --quiet pip && \
    pip install -r requirements.txt # && \
#    pip install -e .
    
ENTRYPOINT python cern_webinfra_inventory_client/app.py
