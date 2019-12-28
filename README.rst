Essoin
======
A SDP (RFC4566) parser. It aims to be as correct as feasible, but also flexible.
Unlike other implementations in similar programming languages, this
implementation does not use any regular expressions and should remain fairly
easy to understand. 

Usage
-----
A not very good example:::

    from essoin import Essoin, SessionDescription

    e = Essoin()
    raw_sdp = 'v=0\n'
    sdp = e.parse(sdp)
    print('{}'.format(sdp.version))

Testing
-------
Unit tests along with fixtures live in `test/` and can be run with:::

    python setup.py test

Unit testing does not aim to be comprehensive, only to be a baseline of testing
against the library against known, or obvious failure cases of intended
behaviour.

Fuzzing
-------
A harness is provided, ensure that pythonfuzz is installed and run:::

    python setup.py fuzz

Crashes should show up in the working directory, corpus data will live in the
`fuzz/` directory. Please report any crashes you find with the crash report and
any other data that may help in reproduction or resolution.

License
-------

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
