declare const FrontifyFinder: any;

window.addEventListener('load', () => {
  const frontifyFieldSelectedClass = 'frontify-image-field--selected';
  const frontifyFields = document.querySelectorAll('.frontify-image-field');
  for (let idx = 0; idx < frontifyFields.length; idx++) {
    const fieldWrapper = frontifyFields[idx];
    const fieldId = fieldWrapper.getAttribute('data-id');
    const fieldDomain = fieldWrapper.getAttribute('data-domain');
    const selectButton = fieldWrapper.querySelector('.frontify-button');
    const imageTag = fieldWrapper.querySelector(
      '.frontify-preview__image'
    ) as HTMLImageElement;
    const nameTag = fieldWrapper.querySelector('.frontify-preview__name');
    const inputField = fieldWrapper.querySelector('#' + fieldId);
    const removeButton = fieldWrapper.querySelector(
      '.frontify-remove-selection'
    );

    const openFrontifyFinder = () => {
      // https://weare.frontify.com/d/3WghAQkakjYf/finder#/frontify-finder/assets-data-structure
      FrontifyFinder.open({
        domain: fieldDomain,
        // container: document.getElementById('FinderWrapper'),
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
              // values: ['eps', 'tif', 'ai'],
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

  // const btn = document.querySelector("#frontify_button");
  // btn.addEventListener("click", evt => {
  //   evt.preventDefault();
  //

  // });
});
