#!/bin/sh

#get_certs_lower=$(echo "$GET_CERTS" | tr '[:upper:]' '[:lower:]')
#
#if [ "$get_certs_lower" = "true" ]; then
#    echo "🆕 Получаем или обновляем сертификаты для доменов: $DOMAIN_MARSEL $DOMAIN_ASIYA $DOMAIN_AMANTUR..."
#
#    # собираем список аргументов -d
#    domains_args=""
#    for domain in $DOMAIN_ASIYA $DOMAIN_MARSEL $DOMAIN_AMANTUR; do
#        domains_args="$domains_args -d $domain"
#    done
#
#    certbot --nginx \
#        --email "$CERTBOT_EMAIL" \
#        --agree-tos \
#        --no-eff-email \
#        --non-interactive \
#        --expand \
#        $domains_args
#
#    nginx -s stop
#    sleep 2
#fi
#
##!/bin/sh

# Convert env variable to lowercase
get_certs_lower=$(echo "$GET_CERTS" | tr '[:upper:]' '[:lower:]')

# Check lowercase value of env variable
if [ "$get_certs_lower" = "true" ]; then

    folder_path="/etc/letsencrypt/live/$DOMAIN_ASIYA"
    # If path exists then let certbot rewrite nginx config
    if [ -d "$folder_path" ]; then
        certbot -n --nginx -d "$DOMAIN_ASIYA"
        nginx -s stop
        # Need time for stop
        sleep 2
    # Else get certs and rewrite nginx config
    else
        certbot --nginx --email "$CERTBOT_EMAIL" --agree-tos --no-eff-email -d "$DOMAIN_ASIYA"
        nginx -s stop
        sleep 2
    fi

fi