/*
  Warnings:

  - Added the required column `subreddit` to the `Post` table without a default value. This is not possible if the table is not empty.

*/
-- RedefineTables
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Post" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "subreddit" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "permalink" TEXT NOT NULL,
    "created" DATETIME NOT NULL
);
INSERT INTO "new_Post" ("created", "id", "permalink", "title") SELECT "created", "id", "permalink", "title" FROM "Post";
DROP TABLE "Post";
ALTER TABLE "new_Post" RENAME TO "Post";
PRAGMA foreign_key_check;
PRAGMA foreign_keys=ON;
