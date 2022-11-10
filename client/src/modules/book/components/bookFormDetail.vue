<template>
  <v-container>
    <v-card v-if="!isLoading">
      <v-card-title>
        <v-row align="center" justify="space-between" no-gutters>
          <v-col class="d-none d-md-block">
            <span class="headline no-split-words">
              {{ $t($route.meta.label) }}
            </span>
          </v-col>

          <v-col class="text-right">
            <v-btn @click="back()">
              <v-icon>arrow_back</v-icon>
              <span class="d-none d-sm-block"> {{ $t("back") }} </span>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-row dense>
          <v-col cols="3" md="2" class="text-left font-weight-bold">
            {{ $t("t_book.prop.isbn") }}:
          </v-col>
          <v-col cols="9" md="10">
            {{ entity.isbn }}
          </v-col>

          <v-col cols="3" md="2" class="text-left font-weight-bold">
            {{ $t("t_book.prop.title") }}:
          </v-col>
          <v-col cols="9" md="10">
            {{ entity.title }}
          </v-col>

          <v-col cols="3" md="2" class="text-left font-weight-bold">
            {{ $t("t_book.prop.category") }}:
          </v-col>
          <v-col cols="9" md="10">
            {{ entity.category }}
          </v-col>

          <v-col cols="3" md="2" class="text-left font-weight-bold">
            {{ $t("t_book.prop.editorial") }}:
          </v-col>
          <v-col cols="9" md="10">
            {{ entity.editorial }}
          </v-col>

          <v-col cols="3" md="2" class="text-left font-weight-bold">
            {{ $t("t_book.prop.price") }}:
          </v-col>
          <v-col cols="9" md="10">
            {{ entity.price }}
          </v-col>

          <v-col cols="3" md="2" class="text-left font-weight-bold">
            {{ $t("t_book.prop.stock") }}:
          </v-col>
          <v-col cols="9" md="10">
            {{ entity.stock }}
          </v-col>

          <v-col cols="3" md="2" class="text-left font-weight-bold">
            {{ $t("t_book.prop.link") }}:
          </v-col>
          <v-col cols="9" md="10">
            {{ entity.link }}
          </v-col>

          <v-col cols="3" md="2" class="text-left font-weight-bold">
            {{ $t("t_book.prop.photo") }}:
          </v-col>
          <v-col cols="9" md="10">
            {{ entity.photo }}
          </v-col>

          <v-col cols="3" md="2" class="text-left font-weight-bold">
            {{ $t("t_book.prop.summary") }}:
          </v-col>
          <v-col cols="9" md="10">
            {{ entity.summary }}
          </v-col>

          <v-col cols="3" md="2" class="text-left font-weight-bold">
            {{ $t("t_book.prop.author") }}:
          </v-col>
          <v-col cols="9" md="10">
            {{ entity.author }}
          </v-col>
          <v-col cols="3" md="2" class="text-left font-weight-bold">
            {{ $t("t_book.prop.source") }}:
          </v-col>
          <v-col cols="9" md="10">
            <span v-if="entity.source">
              {{ $t(`source.${entity.source}`) }}
            </span>
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

import RepositoryFactory from "@/repositories/RepositoryFactory";
const BookEntityRepository = RepositoryFactory.get("BookEntityRepository");

export default {
  name: "bookFormDetail",
  components: { LoadingPage },
  data() {
    return {
      loading: false,
      entity: null,
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
    this._fetchData(this.$route.params.id);
  },
  methods: {
    _fetchData(id) {
      this.loading = true;

      return BookEntityRepository.get(id)
        .then((res) => (this.entity = res))
        .catch((err) => checkInvalidID(err))
        .finally(() => (this.loading = false));
    },
    back() {
      this.$router.push({ name: "Book List", params: { backAction: true } });
    },
  },
};
</script>
