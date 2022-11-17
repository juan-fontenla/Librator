<template>
  <v-container class="book-detail">
    <v-card v-if="!isLoading" class="mt-5">
      <v-card-title>
        <v-row align="center" justify="space-between" no-gutters>
          <v-col class="d-none d-md-block">
            <span class="headline no-split-words">
              {{ $t($route.meta.label) }}
            </span>
          </v-col>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-row class="mt-4 mb-4">
          <v-col class="ml-6" cols="5">
            <v-row v-if="planetaLibroBook.photo || agapeaBook.photo">
              <v-img v-if="planetaLibroBook.photo" class="book-image" max-width="300" :src="planetaLibroBook.photo">
              </v-img>
              <v-img v-else class="book-image" max-width="300" :src="agapeaBook.photo">
              </v-img>
            </v-row>
            <v-row v-else>
              <v-img class="book-image" max-width="300" src="../../../../public/img/default.png">
              </v-img>
            </v-row>
            <v-row class="ml-4 mt-8 font-weight-bold">
              <span>{{ $t('t_book.text.buyOptions') }}</span>
            </v-row>
            <v-row v-if="agapeaBook.price && agapeaBook.link">
              <v-col class="ml-8" cols="3">
                <v-img width="90" height="90" src="../../../../public/img/agapea.png"></v-img>
              </v-col>
              <v-col class="price-link mt-3 ml-3 " cols="3">
                <label class="library-name">{{ $t('t_book.text.agapea') }}</label>
                <label class="mt-2">
                  {{ agapeaBook.price }} €
                </label>
              </v-col>
              <v-col cols="4 ml-7">
                <v-btn icon color="orange" class="mt-4 buy-button" x-large @click="openWindow(agapeaBook.link)">
                  <v-icon x-large>mdi-cart</v-icon>
                </v-btn>
              </v-col>
            </v-row>
            <v-row v-if="planetaLibroBook.price && planetaLibroBook.link" class="mt-6 mb-4">
              <v-col class="ml-8" cols="3">
                <v-img width="90" height="90" src="../../../../public/img/planeta.png"></v-img>
              </v-col>
              <v-col cols="4">
                <v-row class="price-link ml-3 mt-4">
                  <label class="library-name">{{ $t('t_book.text.planetalibro') }}</label>
                  <label class="mt-2">
                    {{ planetaLibroBook.price }} €
                  </label>
                </v-row>
              </v-col>
              <v-col cols="4" align-self="end" class="mb-8">
                <v-btn icon color="orange" class="mt-4 buy-button" x-large @click="openWindow(planetaLibroBook.link)">
                  <v-icon x-large>mdi-cart</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-col>
          <v-col class="mt-6">
            <v-row>
              <span class="book-title">
                {{ planetaLibroBook.title ? planetaLibroBook.title : agapeaBook.title }}
              </span>
            </v-row>
            <v-row>
              <v-col>
                <span class="book-author">
                  {{ planetaLibroBook.author ? planetaLibroBook.author : agapeaBook.author }}
                </span>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="3" md="2" class="text-left font-weight-bold">
                {{ $t("t_book.prop.editorial") }}:
              </v-col>
              <v-col cols="9" md="10">
                {{ planetaLibroBook.editorial ? planetaLibroBook.editorial : agapeaBook.editorial }}
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="3" md="2" class="text-left font-weight-bold">
                {{ $t("t_book.prop.isbn") }}:
              </v-col>
              <v-col cols="9" md="10">
                {{
                    planetaLibroBook.isbn ? planetaLibroBook.isbn : agapeaBook.isbn
                }} </v-col>
            </v-row>
            <v-row>
              <v-col cols="3" md="2" class="text-left font-weight-bold">
                {{ $t("t_book.prop.category") }}:
              </v-col>
              <v-col cols="9" md="10">
                {{ planetaLibroBook.category ? planetaLibroBook.category : agapeaBook.category }}
              </v-col>
            </v-row>
            <v-row class="mt-4" justify="center" cols="9">
              <v-col>
                {{ planetaLibroBook.summary ? planetaLibroBook.summary : agapeaBook.summary }}
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <loading-page v-if="isLoading"></loading-page>
  </v-container>
</template>

<script>
import checkInvalidID from "@/common/checkInvalidID";
import LoadingPage from "@/components/loading-page/LoadingPage.vue";
import bodyBuilder from "bodybuilder";
import RepositoryFactory from "@/repositories/RepositoryFactory";
import mockResponse from "@/common/mock-response"
const BookEntityRepository = RepositoryFactory.get("BookEntityRepository");

export default {
  name: "bookFormDetail",
  components: { LoadingPage },
  data() {
    return {
      loading: false,
      planetaLibroBook: null,
      agapeaBook: null,
    };
  },
  computed: {
    isLoading() {
      return this.loading;
    },
  },
  beforeRouteUpdate(to, from, next) {
    this._fetchData(to.params.id);
    next();
  },
  created() {
    this._fetchData(this.$route.params.isbn);
  },
  methods: {
    async _fetchData(id) {
      this.loading = true;
      let body = bodyBuilder();
      body.query("match", "isbn", id);

      //const response = await BookEntityRepository.getAll(query);

      this.planetaLibroBook = mockResponse.hits.hits.filter(el => el._source.source == 'planetadelibros');
      if (this.planetaLibroBook.length > 0) {
        this.planetaLibroBook = this.planetaLibroBook[0]._source;
        this.planetaLibroBook.category = this.planetaLibroBook.category ? this.planetaLibroBook.category.join(', ') : "";
      }

      this.agapeaBook = mockResponse.hits.hits.filter(el => el._source.source == 'agapea');
      if (this.agapeaBook.length > 0) {
        this.agapeaBook = this.agapeaBook[0]._source;
        this.agapeaBook.category = this.agapeaBook.category ? this.agapeaBook.category.join(', ') : "";
      }
      this.loading = false;
    },
    openWindow(link) {
      window.open(link);
    }
  },
};
</script>
<style scoped>
.book-image {
  margin: auto;
}

.book-title {
  font-weight: bold;
  font-size: 2rem;
}


.theme--light.v-card>.v-card__text,
.theme--light.v-card>.v-card__subtitle {
  color: black !important;
}

.book-author {
  font-size: 1rem;
}

.price-cell {
  border-style: solid;
  background-color: gray;
}

.price-link {
  display: flex;
  flex-direction: column;
}

.library-name {
  font-weight: bold;
}

.buy-button {
  width: 50px !important;
}
</style>