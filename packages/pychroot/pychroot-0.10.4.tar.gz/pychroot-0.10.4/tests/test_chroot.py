import socket
from itertools import chain, cycle
from unittest import mock

from pytest import raises

from pychroot.base import Chroot
from pychroot.exceptions import ChrootError, ChrootMountError


class TestChroot:

    def test_mount(self):
        # testing Chroot.mount()
        with mock.patch('pychroot.base.bind') as bind, \
                mock.patch('os.path.exists') as exists, \
                mock.patch('pychroot.base.dictbool') as dictbool, \
                mock.patch('pychroot.base.simple_unshare'):

            chroot = Chroot('/')
            bind.side_effect = None
            exists.return_value = False
            dictbool.return_value = True
            chroot._mount()
            assert not bind.called

    def test_chroot(self):
        with mock.patch('os.fork') as fork, \
                mock.patch('os.chroot'), \
                mock.patch('os.chdir') as chdir, \
                mock.patch('os.remove') as remove, \
                mock.patch('os._exit'), \
                mock.patch('os.path.exists') as exists, \
                mock.patch('os.waitpid', return_value=(0, 0)), \
                mock.patch('pychroot.utils.mount'), \
                mock.patch('pychroot.base.simple_unshare'):

            # bad path
            exists.return_value = False
            with raises(ChrootError):
                Chroot('/nonexistent/path')
            exists.return_value = True

            # $FAKEVAR not defined in environment
            with raises(ChrootMountError):
                Chroot('/', mountpoints={'$FAKEVAR': {}})

            # no mountpoints
            chroot = Chroot('/', mountpoints=None)
            assert chroot.mountpoints == {}
            assert list(chroot.mounts) == []

            # optional, undefined variable mounts get dropped
            chroot = Chroot('/', mountpoints={
                '$FAKEVAR': {'optional': True},
                '/home/user': {}})
            assert '$FAKEVAR' not in chroot.mounts
            assert len(list(chroot.mounts)) - len(chroot.default_mounts) == 1

            with mock.patch('os.getenv', return_value='/fake/src/path'):
                chroot = Chroot('/', mountpoints={'$FAKEVAR': {}})
            assert '/fake/src/path' in chroot.mountpoints

            exists.side_effect = chain([True], cycle([False]))
            with mock.patch('os.getenv', return_value='/fake/src/path'):
                chroot = Chroot('/', mountpoints={'$FAKEVAR:/fake/dest/path': {}})
            assert chroot.mountpoints['/fake/src/path'].get('create', False)
            exists.side_effect = None
            exists.return_value = True

            # test parent process
            fork.return_value = 10

            # test UTS namespace
            chroot = Chroot('/', hostname='hostname-test')
            with chroot:
                assert socket.gethostname() == 'hostname-test'

            # test child process
            fork.return_value = 0

            chroot = Chroot('/')
            with chroot:
                pass

            # make sure the default mount points aren't altered
            # when passing custom mount points
            default_mounts = dict(Chroot.default_mounts)
            chroot = Chroot('/', mountpoints={'tmpfs:/tmp': {}})
            assert default_mounts == chroot.default_mounts
