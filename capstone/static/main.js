// Javascript Pokemon website that takes in JSON from my own API. EDIT/UPDATE- Heroku deleted the database, JSON will now come from pokeAPI

let obj

async function getText() {
    let x = await fetch('https://pokeapi.co/api/v2/pokemon-species/149/');
    let y = await x.text();
    obj = JSON.parse(y)
    console.log(obj)
    console.log(obj.id)
    console.log(obj.names[8].name)
    console.log("The " + obj.genera[7].genus)
    console.log(obj.flavor_text_entries[1].flavor_text.replaceAll("\n", " "))
  }

async function chooseImages() {
    input = document.getElementById('1stinput')
    image = document.getElementById('1stimage')
    if (input.value > 0) {
      let x = await fetch(`https://pokeapi.co/api/v2/pokemon-species/${input.value}/`);
      let y = await x.text();
      obj = JSON.parse(y)
      image.src = '/static/images/' + input.value + '.gif'
      title1 = document.getElementById('title1')
      title1.innerHTML = obj.names[8].name
      content1 = document.getElementById('content1')
      content1.innerHTML = obj.flavor_text_entries[1].flavor_text.replaceAll("\n", " ").replaceAll("\f", " ")
      number1 = document.getElementById('number1')
      number1.innerHTML = '# ' + obj.id + " The " + obj.genera[7].genus
      // type1 = document.getElementById('type1')
      // type1.innerHTML = 'Type - ' + obj.genera[7].genus
      // weakness1 = document.getElementById('weakness1')
      // weakness1.innerHTML = 'Weaknesses - ' + obj[input.value - 1].weakness
    }

    input = document.getElementById('2ndinput')
    image = document.getElementById('2ndimage')
    if (input.value > 0) {
      let x = await fetch(`https://pokeapi.co/api/v2/pokemon-species/${input.value}/`);
      let y = await x.text();
      obj = JSON.parse(y)
      image.src = '/static/images/' + input.value + '.gif'
      title2 = document.getElementById('title2')
      title2.innerHTML = obj.names[8].name
      content2 = document.getElementById('content2')
      content2.innerHTML = obj.flavor_text_entries[1].flavor_text.replaceAll("\n", " ").replaceAll("\f", " ")
      number2 = document.getElementById('number2')
      number2.innerHTML = '# ' + obj.id + " The " + obj.genera[7].genus
    // type2 = document.getElementById('type2')
    // type2.innerHTML = 'Type - ' + obj[input.value - 1].type
    // weakness2 = document.getElementById('weakness2')
    // weakness2.innerHTML = 'Weaknesses - ' + obj[input.value - 1].weakness
    }


    input = document.getElementById('3rdinput')
    image = document.getElementById('3rdimage')
    if (input.value > 0) {
      let x = await fetch(`https://pokeapi.co/api/v2/pokemon-species/${input.value}/`);
      let y = await x.text();
      obj = JSON.parse(y)
      image.src = '/static/images/' + input.value + '.gif'
      title3 = document.getElementById('title3')
      title3.innerHTML = obj.names[8].name
      content3 = document.getElementById('content3')
      content3.innerHTML = obj.flavor_text_entries[1].flavor_text.replaceAll("\n", " ").replaceAll("\f", " ")
      number3 = document.getElementById('number3')
      number3.innerHTML = '# ' + obj.id + " The " + obj.genera[7].genus
    // type3 = document.getElementById('type3')
    // type3.innerHTML = 'Type - ' + obj[input.value - 1].type
    // weakness3 = document.getElementById('weakness3')
    // weakness3.innerHTML = 'Weaknesses - ' + obj[input.value - 1].weakness
    }
}

function hitEnter() {
    if (event.key === "Enter") {
        chooseImages()
    }
   }

   function mobileFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }

getText()