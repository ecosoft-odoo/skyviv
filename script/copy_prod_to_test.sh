#!/bin/bash
odoo_container_name="skyviv_odoo_1"
postgres_container_name="skyviv_db_1"
postgres="docker exec $postgres_container_name"
filestore_path="/var/lib/docker/volumes/skyviv_filestore/_data/filestore"
database_prod="prod"
database_test="prod_test"
postgres_user="odoo"

echo "============ Start ============"
# Stop odoo
echo "1. Stop $odoo_container_name"
docker stop $odoo_container_name
echo ""

# Restart postgres
echo "2. Restart $postgres_container_name"
docker restart $postgres_container_name
echo ""

# Sleep 1 minute
echo "3. Sleep next command 1 minute"
sleep 60
echo ""

# Drop test database
echo "4. Drop test database: $database_test"
$postgres dropdb -U $postgres_user $database_test
echo ""

# Backup production database
echo "5. Backup production database: $database_prod"
$postgres pg_dump -U $postgres_user -d $database_prod -f backup_$database_prod.sql
echo ""

# Restore test database
echo "6. Restore test database: $database_test"
$postgres createdb -U $postgres_user $database_test
$postgres psql -U $postgres_user -d $database_test -f backup_$database_prod.sql
echo ""

# Remove backup production database file
echo "7. Remove backup_$database_prod.sql"
$postgres rm backup_$database_prod.sql
echo ""

# Disable schedule action
echo "8. Disable schedule action"
$postgres psql -U $postgres_user $database_test -c "update ir_cron set active = False"
echo ""

# Remove outgoing mail server
echo "9. Remove outgoing mail server"
$postgres psql -U $postgres_user $database_test -c "delete from ir_mail_server"
echo ""

# Remove incoming mail server
echo "10. Remove incoming mail server"
$postgres psql -U $postgres_user $database_test -c "delete from fetchmail_server"
echo ""

# Update system parameter
echo "11. Update system parameter"
$postgres psql -U $postgres_user $database_test -c "update ir_config_parameter set value = 'TEST<br/>({db_name})' where key = 'ribbon.name'"
$postgres psql -U $postgres_user $database_test -c "update ir_config_parameter set value = 'http://128.199.109.186' where key = 'web.base.url'"
echo ""

# Copy filestore prod to test
echo "12. Copy filestore prod to test"
rm -r $filestore_path/$database_test
cp -r $filestore_path/$database_prod $filestore_path/$database_test
chown -R 1000 $filestore_path/$database_test
chgrp -R 1000 $filestore_path/$database_test
echo ""

# Start odoo
echo "13. Start $odoo_container_name"
docker start $odoo_container_name
echo ""

echo "============ Finish ============"
