import { fileCreateApi, fileRenameApi, fileUploadApi } from "@/js/api/repository-api.js";

export const getUniqueName = (list, initName, id) => {
    const item = list.find((item) => item.name === initName && item.id && item.id !== id);

    if (item) {
        const last = initName.slice(-1);
        const num = isNaN(parseInt(last)) ? last + "1" : `${parseInt(last) + 1}`;

        return getUniqueName(list, initName.replace(/.$/, num), id);
    }

    return initName;
};

export const renameChildUtil = (
    repositoryId,
    list,
    childId,
    childOldName,
    childNewName,
    parent
) => {
    const file = list.find(
        (file) => file.name === childOldName && (!file.id || file.id === childId)
    );

    childNewName = getUniqueName(list, childNewName, childId);

    if (file) {
        file.name = childNewName;
        file.editActive = false;
        list.sort((file1, file2) => {
            file1.name.localeCompare(file2.name.localeCompare);
        });

        if (file.id && file.id !== "temp") {
            return fileRenameApi(file.id, childNewName)
                .then((res) => {
                    return Promise.resolve(res);
                })
                .catch((err) => {
                    console.log(err);
                    file.name = childOldName;

                    return Promise.reject(err);
                });
        }
        file.id = "temp";

        return fileCreateApi(repositoryId, childNewName, parent, file.fileType)
            .then((res) => {
                file.id = res.id;
                return Promise.resolve(res);
            })
            .catch((err) => {
                console.log(err);
                const index = list.indexOf(2);
                list.splice(index, 1);

                return Promise.reject(err);
            });
    }

    return Promise.reject("Not found");
};

export const mapFiles = (files) => {
    if (!files) return [];

    return files.map((file) => {
        file.editActive = false;
        return file;
    });
};

export const uploadedFileUtil = (repositoryId, parentId, files, fileList) => {
    const promises = [];
    const tempFiles = [];

    for (let i = 0; i < fileList.length; i++) {
        const file = fileList[i];

        const name = getUniqueName([...files, ...tempFiles], file.name, null);
        tempFiles.push({ name: name, id: null });

        promises.push(fileUploadApi(repositoryId, parentId, name, file));
    }

    return Promise.all(promises.map((p) => p.catch((e) => new Error(JSON.stringify(e))))).then(
        (res) => {
            const errors = [];
            console.log(res);

            for (let i in res) {
                if (!(res[i] instanceof Error)) {
                    res[i].editActive = false;
                    files.push(res[i]);
                } else {
                    errors.push(res[i]);
                }
            }

            if (errors.length === 0) return Promise.resolve();

            return Promise.reject(errors.join("; "));
        }
    );
};
