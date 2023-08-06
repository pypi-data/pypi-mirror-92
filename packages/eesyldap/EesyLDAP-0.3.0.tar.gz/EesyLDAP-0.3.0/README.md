# EesyLDAP

This library offer an easy way to manipulate LDAP objects.

## Getting Started

    git clone https://gitlab.easter-eggs.com/brenard/eesyldap.git
    cd eesyldap
    python3 -m venv venv
    source venv/bin/activate
    pip install poetry
    poetry install

See ```doc/quickstart.md``` to learn how to use this library.

## Run tests

To run tests, you need to install eesyldap (see _Getting Started_ section) and run the following command being in the root folder of the project : `pytest --disable-warnings --verbose`

## License
EesyLDAP is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

EesyLDAP is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
