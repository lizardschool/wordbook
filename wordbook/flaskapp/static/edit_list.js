function bloodhound_init(url) {
    var translations = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        limit: 5,
        remote: {
            url: url,
            filter: function (parsedResponse) {
                return $.map(parsedResponse['translations'], function (translation) {
                  // Format verbose output: Apple /ejpl/ - Jabłko
                  verbose = "";
                  verbose += translation['word'] + " ";
                  if (translation['ipa']) {
                      verbose += "/" + translation['ipa'] + "/";
                  }
                  if (translation['simplified']) {
                      verbose += "[" + translation['simplified'] + "]";
                  }
                  verbose += " - ";
                  verbose += translation['translation'];

                  return {
                      id: translation['id'],
                      value: verbose,
                      word: translation['word'],
                      ipa: translation['ipa'],
                      simplified: translation['simplified'],
                      translation: translation['translation']
                  };
              });
            }
          }
    });

  translations.initialize();
  return translations
}

function get_typeahead() {
   return $('#word-box .typeahead');
}

function init_typeahead() {
  get_typeahead().typeahead({
    hint: true,
    highlight: true,
    minLength: 1
  },
  {
    name: 'translations',
    displayKey: 'value',
    // `ttAdapter` wraps the suggestion engine in an adapter that
    // is compatible with the typeahead jQuery plugin
    source: translations.ttAdapter(),
    templates: {
      empty: [
        '<div class="empty-message">',
        'Unable to find any word that match the current query.',
        '</div>'
      ].join('\n'),
      footer: [
        '<div>',
        '<button data-toggle="modal" data-target="#addWordModal" onclick="open_add_word_modal()" class="btn btn-primary">Add new translation</button>',
        '</div>'
      ].join('\n'),
      suggestion: Handlebars.compile('<p><strong>{{ word }}</strong> <em>/{{ ipa }}/ [{{ simplified }}]</em>– {{ translation }}</p>')
    }
  })
}


// opens modal with form where user can add new translation
function open_add_word_modal() {
    // rewrite word from typeahead to input in modal
    var word = $('#word-box .typeahead').typeahead('val');
    $('#wordInput').val(word);
    // close typeahead
    $('#word-box .typeahead').typeahead('close');
    $('#word-box .typeahead').typeahead('val', '');
}

// cardlist_id is included already in url
function add_word_to_list(url, translation_id, done_func, fail_func) {
    // alert('add word to list called');
    $.ajax({
        type: 'POST',
        url: url,
        data: {translation_id: translation_id},
        dataType: 'json'
    }).done(function(data, textStatus, jqXHR){
        console.log(data);
        $('#cardsTable').DataTable().ajax.reload();
        $('#word-box .typeahead').typeahead('val', '');
        //$('#cardsTable').DataTable().row.add(data.translation);
        // done_func(data); // don't know why this function isn't called
    }).fail(function(data, textStatus, jqXHR){
        alert('adtl fail');
        fail_func(data);
    });
}

/*
 * edit_list po zaladowaniu strony robi request o slowka
 * jesli dodajemy nowe slowo do listy to modyfikujemy zaladowana do pamieci liste
 * wstawiajac na pierwszej pozycji zwrocony obiekt dto
 * a z ostatniej pozycji wywalamy istniejacy tam obiekt
 *
 */
function post_new_translation(post_url, done_func, fail_func) {
    var formData = {
        'word': $('input[name=word]').val(),
        'ipa': $('input[name=ipa]').val(),
        'simplified': $('input[name=simplified]').val(),
        'translation': $('textarea[name=translation]').val(),
        'from_language': 'en',  // TODO: cardlist object should contain this information
        'into_language': 'pl'  // TODO: as above
    };

    $.ajax({
      type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
      url: post_url, // the url where we want to POST
      data: formData, // our data object
      dataType: 'json', // what type of data do we expect back from the server
      encode: true

    }).done(function(data, textStatus, jqXHR){
        done_func(data);
    }).fail(function(data, textStatus, jqXHR){
        fail_func(data);
    });
}
