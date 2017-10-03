PYTHON_MODULES=asmminator

PYTHON_VERSION?=2.7.5
PYWIN32_VERSION = 218
PYGAME_VERSION = 1.9.1
PYWIN32=pywin32-${PYWIN32_VERSION}.win32-py2.7.exe
PYINSTALLER_VERSION?=3.1
PYGAME_MSI=pygame-${PYGAME_VERSION}.win32-py2.7.msi
WXPYTHON_INSTALLER=wxPython3.0-win32-3.0.2.0-py27.exe

WGET?=wget -q

VIRTUALENV_ARGS=--system-site-packages
MAKERY_URL=https://raw.githubusercontent.com/gutomaia/makery/master

OK=\033[32m[OK]\033[39m
FAIL=\033[31m[FAIL]\033[39m
CHECK=@if [ $$? -eq 0 ]; then echo "${OK}"; else echo "${FAIL}" ; fi

default: python.mk pyinstaller.mk
	@$(MAKE) -C . run

ifeq "true" "${shell test -f python.mk && echo true}"
include python.mk
endif

ifeq "true" "${shell test -f pyinstaller.mk && echo true}"
include pyinstaller.mk
endif

python.mk:
	@${WGET} ${MAKERY_URL}/python.mk && touch $@

pyinstaller.mk:
	@${WGET} ${MAKERY_URL}/pyinstaller.mk && touch $@


ifeq "Darwin" "$(shell uname)"
PYTHON=arch -i386 python
PYTHON=python2.7-32
else
PYTHON=python
endif

${DOWNLOAD_PATH}/${PYGAME_MSI}: ${DOWNLOAD_CHECK}
	@cd ${DOWNLOAD_PATH} && \
		${WGET} http://pygame.org/ftp/${PYGAME_MSI}
	@touch $@

${DOWNLOAD_PATH}/pygame.installed: ${PYTHON_EXE} ${DOWNLOAD_PATH}/${PYGAME_MSI}
	@cd ${DOWNLOAD_PATH} && \
		msiexec /i ${PYGAME_MSI} /qb
	@touch $@

${DOWNLOAD_PATH}/${WXPYTHON_INSTALLER}: ${DOWNLOAD_CHECK}
	@cd ${DOWNLOAD_PATH} && \
		${WGET} http://downloads.sourceforge.net/wxpython/${WXPYTHON_INSTALLER}
	@touch $@

${DOWNLOAD_PATH}/wxpython.installed: ${PYTHON_EXE} ${DOWNLOAD_PATH}/${WXPYTHON_INSTALLER}
	@cd ${DOWNLOAD_PATH} && \
		wine ${WXPYTHON_INSTALLER} /SP- /VERYSILENT
	@touch $@

build_tools: tools/pyinstaller-${PYINSTALLER_VERSION}/pyinstaller.py

build: python_build

run: build
	${VIRTUALENV} ${PYTHON} ${PYTHON_MODULES}/app.py

run_win:
	@wine ${PYTHON_EXE} ${PYTHON_MODULES}/app.py

dist/darwin/${PYTHON_MODULES}: ${PYINSTALLER}
	${PYTHON} -O ${PYINSTALLER} --onedir  ${PYTHON_MODULES}.darwin.spec

dist/linux/${PYTHON_MODULES}: ${PYINSTALLER}
	${PYTHON} -O ${PYINSTALLER} --onedir  ${PYTHON_MODULES}.linux.spec

windows: ${PYINSTALLER} ${PYTHON_EXE} ${WINDOWS_BINARIES} ${TOOLS_PATH}/requirements.windows.check ${DOWNLOAD_PATH}/pygame.installed ${DOWNLOAD_PATH}/wxpython.installed
	@rm -rf dist/windows
	@mkdir -p dist/windows
	@wine ${PYTHON_EXE} ${PYINSTALLER} --onefile ${PYTHON_MODULES}.windows.spec --distpath dist/windows

run_dwin: windows
	cd dist/windows/asmminator && wine asmminator.exe

dist/asmminator.zip: windows
	cd dist/windows && \
		zip -r asmminator.zip asmminator

dist: windows

distribute: dist/asmminator.zip

clean: python_clean
	@rm -rf tools
	@rm -rf reports

purge: clean python_purge
	@rm python.mk
	@rm pyinstaller.mk
	@rm -rf deps
	@rm -rf ${WINE_PATH}
	@rm -rf .downloads
	@rm -rf .tools

.PHONY: clean run dist report
