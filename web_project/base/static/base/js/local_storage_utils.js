
class LocalSorageManager {
    saveItem(key, item) {
        localStorage.setItem(key, item);
    }

    getItem (key) {
        return localStorage.getItem(key);
    }

    removeItem(key) {
        localStorage.removeItem(key);
    }
}
