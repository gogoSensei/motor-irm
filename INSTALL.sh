# para gtk+ &gtk objets
sudo apt install apt-file docbook docbook-xsl build-essential git-core gettext libtext-csv-perl autotools-dev autoconf gettext pkgconf autopoint yelp-tools libjson-pp-perl libfile-copy-recursive-perl

sudo apt-file update
mkdir -p ~/jhbuild/checkout
cd ~/jhbuild/checkout
git clone https://gitlab.gnome.org/GNOME/jhbuild.git
cd jhbuild
./autogen.sh --simple-install
make
make install

echo 'PATH=~/.local/bin:$PATH' >> ~/.bashrc; . ~/.bashrc

jhbuild sysdeps --install
jhbuild sanitycheck
jhbuild build gtk+
