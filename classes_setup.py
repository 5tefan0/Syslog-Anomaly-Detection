

class Template(object):
    def __init__(self, index, words):
        self._index = index
        self._words = words
        self._nwords = len(words)
        self._counts = 0
        self._line_indeces = []
        self._window_five = [ [1,0,0],[2,0,0],[3,0,0],[4,0,0],[5,0,0]  ]
        # self._window_five = [ (1st ranked, template index, average appearence with decaying weights), ... , 5th ranked  ];
        #then define the updating function of the window
        #in test(line) then define the function that compares the new line (with the previous five) with the window
        #do the same for window_ten, window_fifty, window_onehundred
        #[ [],[],[],[],[]  ]

    @property
    def index(self):
        return self._index

    @property
    def words(self):
        return self._words

    @property
    def nwords(self):
        return self._nwords

    @property
    def counts(self):
        return self._counts

    @property
    def line_indeces(self):
        return self._line_indeces



    def get_similarity_score(self, new_words):
        """Retruens a similarity score.

        Args:
          new_words: An array of words.

        Returns:
          score: in float.
        """
        assert(False)

    def update(self, new_words):
        """Updates the template data using the supplied new_words.
        """
        assert(False)

    def __str__(self):
        template = ' '.join([self.words[idx] if self.words[idx] != '' else '*' for idx in range(self.nwords)])
        return '{index}({nwords})({counts}):{template}'.format(
            index=self.index,
            nwords=self.nwords,
            counts=self._counts,
            template=' '.join([self.words[idx] if self.words[idx] != '' else '*' for idx in range(self.nwords)]))

class TemplateManager(object):
    def __init__(self):
        self._templates = []

    @property
    def templates(self):
        return self._templates

    def infer_template(self, words):
        """Infer the best matching template, or create a new template if there
        is no similar template exists.

        Args:
          words: An array of words.

        Returns:
          A template instance.

        """
        assert(False)

    def _append_template(self, template):
        """Append a template.

        Args:
          template: a new template to be appended.

        Returns:
          template: the appended template.
        """
        assert(template.index == len(self.templates))
        self.templates.append(template)
        return template
