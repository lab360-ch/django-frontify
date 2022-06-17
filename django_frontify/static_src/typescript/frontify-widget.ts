// import {create} from '@frontify/frontify-finder';
declare const FrontifyFinder: any;

export {};
declare global {
  interface Window {
    FrontifyFinder: any;
  }
}

window.addEventListener('load', () => {
  const frontifyFieldSelectedClass = 'frontify-image-field--selected';
  const frontifyFields = document.querySelectorAll('.frontify-image-field');

  for (let idx = 0; idx < frontifyFields.length; idx++) {
    const fieldWrapper = frontifyFields[idx];
    const fieldId = fieldWrapper.getAttribute('data-id');
    const fieldDomain = fieldWrapper.getAttribute('data-domain');
    const fieldClientId = fieldWrapper.getAttribute('data-client-id');
    const selectButton = fieldWrapper.querySelector('.frontify-button');
    const imageTag = fieldWrapper.querySelector(
      '.frontify-preview__image'
    ) as HTMLImageElement;
    const nameTag = fieldWrapper.querySelector('.frontify-preview__name');
    const inputField = fieldWrapper.querySelector('#' + fieldId);
    const removeButton = fieldWrapper.querySelector(
      '.frontify-remove-selection'
    );
    const finderVersion = fieldWrapper.getAttribute('data-finder-version');

    const openFrontifyFinder = async () => {
      switch (finderVersion) {
        case "1":
          openFrontifyFinderV1();
          break;
        case "2":
          openFrontifyFinderV2();
          break;
        default:
          alert("Invalid Finder version specified in DJANGO_FRONTIFY_FINDER_VERSION")
      }
    }

    const openFrontifyFinderV1 = () => {
      FrontifyFinder.open({
        domain: fieldDomain,
        success: assets => {
          const asset = assets[0];
          console.log(asset);
          fieldWrapper.classList.add(frontifyFieldSelectedClass);
          imageTag.src = asset.generic_url.split('?')[0] + '?height=36';
          nameTag.innerHTML = asset.name || asset.title;

          inputField.innerHTML = JSON.stringify(asset, null, 4);
        },
        cancel: () => {
          console.log('Selection cancelled!');
        },
        error: message => {
          console.log(`Error:`, message);
          if (message.code === "ERR_FINDER_MESSAGE") {
            const msgJson = JSON.parse(message.message);
            if (msgJson.readyState === 4 && msgJson.responseJSON.error.includes("Access token expired")) {
              console.warn("Access Token expired");
              console.log(localStorage.getItem("FrontifyFinder_token"))
              if (localStorage.getItem("FrontifyFinder_token")) {
                console.log("Token found. Clear token and start finder again.")
                FrontifyFinder.close();
                localStorage.removeItem("FrontifyFinder_token");
                openFrontifyFinder();
              }
            }
          }
        },
        warning: message => {
          console.log(`Warning:`, message);
          if (message.code === "WARN_AUTH_OPTIONS") {
            console.log('WARN_AUTH_OPTIONS ...')
            if (localStorage.getItem("FrontifyFinder_token")) {
              console.log("Token found. Clear token and start finder again.")
              FrontifyFinder.close();
              localStorage.removeItem("FrontifyFinder_token");
              openFrontifyFinder();
            }
          }
        },
        settings: {
          multiSelect: false,
          filters: [
            {
              key: 'object_type',
              values: ['IMAGE'],
              inverted: false
            },
            {
              key: 'ext',
              values: ['eps', 'ai'],
              inverted: true
            }
          ],
          popup: {
            title: 'My Company\'s Frontify Assets',
            size: {
              width: 600,
              height: 400
            },
            position: {
              x: 50,
              y: 50
            }
          }
        }
      });
    }


    const openFrontifyFinderV2 = async () => {
      try {
        const finder = await window.FrontifyFinder.create({
          clientId: fieldClientId,
          domain: fieldDomain,
          options: {
            allowMultiSelect: false,
            permanentDownloadUrls: true
          }
        });

        finder.onAssetsChosen(assets => {
          const asset = assets[0];
          fieldWrapper.classList.add(frontifyFieldSelectedClass);
          imageTag.src = asset.previewUrl.split('?')[0] + '?height=36';
          nameTag.innerHTML = asset.name || asset.title;
          inputField.innerHTML = JSON.stringify(asset, null, 4);
          finder.close();
          fieldWrapper.parentElement.classList.remove('frontify-modal-open');
        });

        finder.onCancel(() => {
          finder.close();
          fieldWrapper.parentElement.classList.remove('frontify-modal-open');
        });

        finder.mount(fieldWrapper.parentElement.querySelector('.frontify-modal'));
        fieldWrapper.parentElement.classList.add('frontify-modal-open');

      } catch(error) {
        // Log error
        console.log(error);
      }
    }

    removeButton.addEventListener('click', event => {
      event.preventDefault();
      fieldWrapper.classList.remove(frontifyFieldSelectedClass);
      imageTag.src = '';
      nameTag.innerHTML = '';
      inputField.innerHTML = '';
    });

    selectButton.addEventListener('click', event => {
      event.preventDefault();
      openFrontifyFinder();
    });
  }
});
