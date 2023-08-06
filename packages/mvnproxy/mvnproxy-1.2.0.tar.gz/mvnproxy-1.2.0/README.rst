Maven local proxy.

Installation
============

.. code:: sh

    pip install mvnproxy

Configuration
=============

To configure ``mvnproxy`` you need to at least specify some mirrors to
be used. The full list of configurable parameters is visible here:

.. code:: yaml

    host: 0.0.0.0
    port: 6990
    cache_folder: /home/raptor/tmp/mvnproxy
    mirrors:
    - url: https://repo.maven.apache.org/maven2
    - url: http://repo1.sample.net/artifactory/cool-artifacts/
    - url: https://secure-repo2.sample.net/nexus3/also-cool/
      auth:
        user: myuser
        pass: {USER_PASS}

Each mirror in turn supports ``auth`` configuration where the user and
pass can be specified. If no ``auth`` is specified, it simply does
unauthenticated requests.

Environment variables such as the ``USER_PASS`` can be interpolated in
the configuration using the curly bracket notation.

Maven Configuration
===================

Maven also needs to be configured in oredr to use the ``mvnproxy``. To
see the required configuration you can either open the
http://localhost:6990/ or just use in the ``.m2/settings.xml``:

.. code:: xml

    <settings>
      <mirrors>
        <mirror>
          <id>central</id>
          <name>central</name>
          <url>http://localhost:6990/repo</url>
          <mirrorOf>*</mirrorOf>
        </mirror>
      </mirrors>
      <profiles>
        <profile>
          <activation>
            <activeByDefault>true</activeByDefault>
          </activation>
          <repositories>
            <repository>
              <id>central</id>
              <name>central</name>
              <url>http://localhost:6990/repo</url>
              <releases>
                <enabled>true</enabled>
              </releases>
              <snapshots>
                <enabled>true</enabled>
              </snapshots>
            </repository>
          </repositories>
        </profile>
      </profiles>
    </settings>
