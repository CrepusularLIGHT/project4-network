document.addEventListener('DOMContentLoaded', () => {

    // Button to like post
    document.querySelectorAll('.likeForm').forEach(form => {

        const button_like = form.children[0];

        button_like.addEventListener('click', () => {

            if (button_like.dataset.liked == 'false') {

                const postId = button_like.dataset.post;
                const sessionUser = button_like.dataset.sessionUser;
                const fetchURL = '/like/' + postId + '/' + sessionUser;
                var likes = Number(button_like.dataset.likes);

                fetch(fetchURL)
                    .then(response => {
                        console.log(response);
                        return response.text()
                    })
                    .catch(err => {
                        alert(err);
                    })

                button_like.setAttribute('data-liked', 'true');
                button_like.setAttribute('class', 'btn btn-primary');

                likes += 1;
                button_like.setAttribute('data-likes', likes);
                button_like.innerHTML = '<i class="fa fa-thumbs-up"></i> ' + likes;

            } else {

                const postId = button_like.dataset.post;
                const sessionUser = button_like.dataset.sessionUser;
                const fetchURL = '/unlike/' + postId + '/' + sessionUser;
                var likes = Number(button_like.dataset.likes);

                fetch(fetchURL)
                    .then(response => {
                        console.log(response);
                        return response.text()
                    })
                    .catch(err => {
                        alert(err);
                    })

                button_like.setAttribute('data-liked', 'false');
                button_like.setAttribute('class', 'btn btn-outline-primary');

                likes -= 1;
                button_like.setAttribute('data-likes', likes);
                button_like.innerHTML = '<i class="fa fa-thumbs-up"></i> ' + likes;
            }
        });
    });

    // Button to delete post
    document.querySelectorAll('.delete-button').forEach(button_delete => {

        button_delete.addEventListener('click', () => {

            console.log('delete button pressed');

            const postId = button_delete.dataset.post;
            const postId_ul_class = '.post-' + postId;
            const postId_hr_class = '.hr-' + postId;
            const fetchURL = '/delete/' + postId;

            console.log(postId);
            console.log(fetchURL);

            fetch(fetchURL)
                .then(response => {
                    console.log(response);
                    return response.text()
                })
                .catch(err => {
                    alert(err);
                })

            const post_element = document.querySelector(postId_ul_class);
            const hr_element = document.querySelector(postId_hr_class);
            post_element.setAttribute('style', 'display:none');
            button_delete.setAttribute('style', 'display:none');
            hr_element.setAttribute('style', 'display:none');
        })
    })
})