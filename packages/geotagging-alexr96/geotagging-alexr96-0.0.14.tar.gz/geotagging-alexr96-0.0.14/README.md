
<h1 class="text-pink">Database Package for Geotag Project</h1>
This is a package to help manage the database for DevPipeline's geotagging project, it containse dataclass functionallity and functions for database creation and updating.

<h2>Database Creation</h2>
<ol>
<li>
First make sure that postgress is downloaded <code>$ psql</code>, if not - 
<code>$ brew install postgresql</code>
<ul>
**If you do not have Brew:**
<li>
<code>$ /bin/bash -c "$(curl -fsSL h<span>ttps:/</span>/raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"</code>
</li>
<li>
<code>$ brew install postgresql</code>
</li>
<li>
Then run the command 
<code>$ pg_ctl -D /usr/local/var/postgres start</code>
to start postgres
</li>
</ul>
</li>
<li>
Download the package at %3CPIP LINK HERE%3E
</li>
<li>
Open the python interpreter and run 
<code>import %3NAME_HERE%3E</code> then
<code>NAME_HERE.db_ops.create_db(username=YOUR_PSQL_USERNAME, passwork=YOUR_PSQL_PASSWORD)</code> then
<code>NAME_HERE.db_ops.update_db()</code>
</li>
</ol>